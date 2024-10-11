import subprocess
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import CompiledCode
from django.template import RequestContext

def home_page(request):
    return render(request, 'home/front_page.html')

@login_required
def runcode(request):
    if request.method == "POST":
        codeareadata = request.POST['codearea']
        inputdata = request.POST.get('input', '')
        language = request.POST.get('language', 'python')

        if language == 'cpp':
            output = run_cpp_code(codeareadata, inputdata)
        else:
            output = run_python_code(codeareadata, inputdata)

        # Save the compiled code
        CompiledCode.objects.create(
            user=request.user,
            language=language,
            code=codeareadata
        )

        context = {
            "code": codeareadata,
            "output": output,
            "language": language
        }
        return render(request, 'home/front_page.html', context)

    return render(request, 'home/front_page.html')

@login_required
def recent_codes(request):
    recent_codes = CompiledCode.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'home/recent_codes.html', {'recent_codes': recent_codes})

def run_cpp_code(code, input_data):
    # Path to store the temporary code file and compiled output
    cpp_file_path = os.path.join(settings.BASE_DIR, 'temp_code.cpp')
    compiled_file_path = os.path.join(settings.BASE_DIR, 'temp_code.out')

    try:
        # Step 1: Write C++ code to a temporary file
        with open(cpp_file_path, 'w') as cpp_file:
            cpp_file.write(code)

        # Step 2: Compile the C++ code using g++
        compile_process = subprocess.run(['g++', cpp_file_path, '-o', compiled_file_path],
                                         capture_output=True, text=True)

        # Step 3: Check if there are any compilation errors
        if compile_process.returncode != 0:
            output = compile_process.stderr  # Compilation error output
        else:
            # Step 4: If compilation succeeds, execute the compiled file
            execution_process = subprocess.run([compiled_file_path],
                                               input=input_data,
                                               capture_output=True,
                                               text=True)

            # Step 5: Get the program's output or runtime error
            if execution_process.returncode != 0:
                output = execution_process.stderr  # Runtime error output
            else:
                output = execution_process.stdout  # Successful output

    except Exception as e:
        output = str(e)

    finally:
        # Clean up temporary files
        if os.path.exists(cpp_file_path):
            os.remove(cpp_file_path)
        if os.path.exists(compiled_file_path):
            os.remove(compiled_file_path)

    return output

def run_python_code(code, input_data):
    import sys
    import io

    try:
        # Save original standard output and input references
        original_stdout = sys.stdout
        original_stdin = sys.stdin

        # Redirect stdout to a string buffer
        sys.stdout = io.StringIO()

        # Redirect stdin to a string buffer with user input
        sys.stdin = io.StringIO(input_data)

        # Execute the provided Python code
        exec(code)

        # Get the output from stdout
        output = sys.stdout.getvalue()

        # Reset stdin and stdout to their original values
        sys.stdout = original_stdout
        sys.stdin = original_stdin

    except Exception as e:
        output = str(e)

    return output