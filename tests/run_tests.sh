#!/bin/bash
# Test runner script for Study Helper workflow

set -e

echo "================================"
echo "Study Helper Workflow Test Suite"
echo "================================"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest is not installed"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo "📦 Dependencies installed"
echo ""

# Run schema validation tests
echo "🔍 Running Schema Validation Tests..."
pytest test_workflow_schema.py -v
echo ""

# Run unit tests
echo "🧪 Running Unit Tests..."
pytest unit/ -v
echo ""

# Run integration tests
echo "🔗 Running Integration Tests..."
pytest integration/ -v
echo ""

# Generate coverage report
echo "📊 Generating Coverage Report..."
pytest --cov=. --cov-report=term-missing --cov-report=html
echo ""

echo "✅ All tests completed!"
echo ""
echo "📈 Coverage report generated in htmlcov/index.html"