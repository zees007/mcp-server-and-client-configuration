from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"Adding {a} and {b}")
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print(f"Multiplying {a} and {b}")
    return a * b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print(f"Subtracting {a} and {b}")
    return a - b    

@mcp.tool()
def divide(a: int, b: int) -> int:
    """Divide two numbers"""
    print(f"Dividing {a} and {b}")
    return a / b

@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print(f"Power of {a} and {b}")
    return a ** b

@mcp.tool()
def modulo(a: int, b: int) -> int:
    """Modulo of two numbers"""
    print(f"Modulo of {a} and {b}")
    return a % b

if __name__ == "__main__":
    mcp.run(transport="stdio")

