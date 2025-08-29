# 🧪 Testing Guide for Personal Financial Advisor

This directory contains comprehensive tests for the Personal Financial Advisor application. The test suite is designed to help students verify their implementation and learn testing best practices.

## 📋 Test Coverage

The test suite covers:

- **🤖 AI Agents**: All agent classes and their creation
- **🔌 MCP Server**: Database tools and error handling
- **🛠️ Utilities**: Database connections, logging, and configuration
- **🎨 UI Components**: Streamlit components and utilities
- **🔗 Integration**: Agent collaboration and data flow

## 🚀 Running Tests

### Prerequisites

1. **Activate your virtual environment**:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Install testing dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Option 1: Run All Tests (Recommended)

```bash
# From project root
python tests/run_tests.py

# Or using pytest directly
pytest tests/ -v
```

### Option 2: Run Specific Test Categories

```bash
# Test only agents
pytest tests/test_agents.py -v

# Test only MCP server
pytest tests/test_mcp_server.py -v

# Test only utilities
pytest tests/test_utils.py -v

# Test only UI components
pytest tests/test_ui_components.py -v
```

### Option 3: Run Tests by Markers

```bash
# Run only unit tests
pytest tests/ -m unit -v

# Run only integration tests
pytest tests/ -m integration -v

# Skip slow tests
pytest tests/ -m "not slow" -v
```

### Option 4: Run Individual Test Classes

```bash
# Test specific agent class
pytest tests/test_agents.py::TestSpendingAnalyzerAgent -v

# Test specific test method
pytest tests/test_agents.py::TestSpendingAnalyzerAgent::test_create_spending_analyzer_agent -v
```

## 📊 Test Results

When tests run successfully, you'll see:

```
🧪 Running Personal Financial Advisor Test Suite
============================================================
test_create_spending_analyzer_agent (__main__.TestSpendingAnalyzerAgent) ... ok
test_create_goal_planner_agent (__main__.TestGoalPlannerAgent) ... ok
test_create_advisor_agent (__main__.TestAdvisorAgent) ... ok
...

============================================================
📊 Test Results Summary
Tests run: 25
Failures: 0
Errors: 0

✅ All tests passed successfully!
```

## 🎯 What Each Test Verifies

### `test_agents.py`
- ✅ Agent creation functions work correctly
- ✅ MCP toolsets are properly configured
- ✅ Agent instructions and descriptions are set
- ✅ Multi-agent orchestration setup

### `test_mcp_server.py`
- ✅ FastMCP server starts successfully
- ✅ All database tools are registered
- ✅ Database operations work through MCP
- ✅ Error handling is graceful

### `test_utils.py`
- ✅ Database connections establish properly
- ✅ Logging configuration works
- ✅ Environment variables are handled
- ✅ UI utilities function correctly

### `test_ui_components.py`
- ✅ All UI components can be imported
- ✅ Component functions are callable
- ✅ Data handling is robust
- ✅ Chart generation works

## 🔧 Test Configuration

### `conftest.py`
This file provides:
- **Common fixtures** for all tests
- **Mock objects** for external dependencies
- **Test data** samples
- **Pytest configuration** and markers

### Key Fixtures
- `mock_db_connection`: Mock database connection
- `sample_customer_data`: Test customer data
- `mock_google_adk_components`: Mock ADK classes
- `mock_environment_variables`: Test environment config

## 🐛 Troubleshooting Tests

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the project root
   cd /path/to/agent-ai-personal-financial-advisor
   
   # Activate virtual environment
   source venv/bin/activate
   ```

2. **Missing Dependencies**
   ```bash
   # Install all requirements including test dependencies
   pip install -r requirements.txt
   ```

3. **Database Connection Errors**
   - Tests use mocked database connections
   - No actual MySQL server needed for unit tests
   - Integration tests may require database setup

4. **Streamlit Import Errors**
   - UI component tests handle Streamlit gracefully
   - Some tests may show Streamlit warnings (expected)

### Test Debugging

```bash
# Run with maximum verbosity
pytest tests/ -vvv

# Stop on first failure
pytest tests/ -x

# Show local variables on failure
pytest tests/ --tb=long

# Run with print statements visible
pytest tests/ -s
```

## 📈 Test Metrics

### Coverage Goals
- **Unit Tests**: 90%+ coverage
- **Integration Tests**: Core functionality covered
- **Error Handling**: All error paths tested
- **Edge Cases**: Boundary conditions verified

### Performance Targets
- **Test Suite**: < 30 seconds total
- **Individual Tests**: < 2 seconds each
- **Setup/Teardown**: < 1 second per test

## 🎓 Learning Objectives

Running these tests helps students learn:

1. **Testing Best Practices**
   - Unit testing with unittest/pytest
   - Mocking external dependencies
   - Test organization and naming

2. **AI Agent Testing**
   - Testing agent creation and configuration
   - Verifying tool integration
   - Multi-agent system validation

3. **MCP Protocol Testing**
   - Testing MCP server functionality
   - Database tool verification
   - Error handling validation

4. **UI Component Testing**
   - Component import verification
   - Function signature validation
   - Data handling robustness

## 🔄 Continuous Testing

### Development Workflow
1. **Write code** for new features
2. **Run tests** to verify functionality
3. **Fix any failures** before committing
4. **Add new tests** for new features

### Pre-commit Checklist
- [ ] All existing tests pass
- [ ] New functionality has tests
- [ ] No test warnings or errors
- [ ] Test coverage maintained

## 📚 Additional Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **Unittest Documentation**: https://docs.python.org/3/library/unittest.html
- **Mock Documentation**: https://docs.python.org/3/library/unittest.mock.html
- **Testing Best Practices**: https://realpython.com/python-testing/

---

**Happy Testing! 🧪✨**

Remember: Good tests are like good documentation - they help you and others understand how your code works and catch bugs before they reach production.
