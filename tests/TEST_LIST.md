# Complete Test List

## All Tests (23 total)

### Schema Validation Tests (9 tests)
**File**: `test_workflow_schema.py`

1. `test_workflow_file_exists` - Verifies workflow YAML file exists
2. `test_workflow_is_valid_yaml` - Validates YAML syntax
3. `test_required_top_level_fields` - Checks required fields present
4. `test_workflow_id` - Validates workflow ID
5. `test_workflow_namespace` - Validates namespace
6. `test_inputs_structure` - Checks input definitions
7. `test_tasks_structure` - Validates task structure
8. `test_expected_tasks_present` - Ensures all tasks exist
9. `test_conditional_task_structure` - Validates If task logic

### Unit Tests (12 tests)

#### Fetch Data Tests (3 tests)
**File**: `unit/test_fetch_data_logic.py`

10. `test_successful_data_fetch` - Tests successful HTTP GET
11. `test_fetch_with_http_error` - Tests HTTP error handling
12. `test_fetch_empty_content` - Tests empty response handling

#### AI Analysis Tests (2 tests)
**File**: `unit/test_ai_analysis_logic.py`

13. `test_successful_ai_analysis` - Tests HuggingFace API interaction
14. `test_prompt_construction` - Validates prompt formatting

#### JSON Parsing Tests (3 tests)
**File**: `unit/test_parse_json_logic.py`

15. `test_parse_clean_json` - Tests clean JSON parsing
16. `test_parse_json_with_leading_text` - Tests JSON extraction from text
17. `test_no_json_in_output` - Tests missing JSON handling

#### YouTube Search Tests (2 tests)
**File**: `unit/test_youtube_search_logic.py`

18. `test_successful_youtube_search` - Tests SerpAPI video search
19. `test_youtube_search_with_no_results` - Tests empty results

#### Final Output Tests (2 tests)
**File**: `unit/test_final_output_logic.py`

20. `test_output_with_all_fields` - Tests TOUGH path output
21. `test_output_without_video_fields` - Tests SIMPLE path output

### Integration Tests (2 tests)
**File**: `integration/test_workflow_integration.py`

22. `test_complete_tough_workflow` - End-to-end TOUGH path
23. `test_complete_simple_workflow` - End-to-end SIMPLE path

## Run Individual Tests

```bash
# Run a specific test
pytest test_workflow_schema.py::TestWorkflowSchema::test_workflow_id -v

# Run all tests in a file
pytest unit/test_fetch_data_logic.py -v

# Run all unit tests
pytest unit/ -v

# Run all integration tests
pytest integration/ -v

# Run all tests
pytest -v
```