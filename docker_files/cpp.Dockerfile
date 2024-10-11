# Use the official GCC compiler image
FROM gcc:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the code into the container
COPY code.cpp .

# Compile the C++ code and run the binary
RUN g++ code.cpp -o output
CMD ["./output"]
