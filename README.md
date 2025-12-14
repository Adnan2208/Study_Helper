# Study Helper

A Kestra-based intelligent workflow automation platform that transforms study materials into personalized learning plans. Study Helper analyzes documents from Google Drive, generates AI-powered summaries, creates structured study schedules, and curates relevant video resources to optimize your learning experience.

## Overview

Study Helper leverages advanced orchestration and AI capabilities to streamline exam preparation. The platform automatically extracts content from multiple file formats (PDF, DOCX, TXT), performs intelligent analysis to assess difficulty and identify key concepts, generates progressive study plans tailored to your schedule, and provides supplementary learning resources—all delivered through beautifully formatted reports.

## Features

- **Multi-Format Content Extraction**: Automatically processes PDF, DOCX, and text files from Google Drive
- **AI-Powered Analysis**: Utilizes HuggingFace models to analyze content difficulty, extract topics, and identify key concepts
- **Intelligent Study Planning**: Generates personalized day-by-day study schedules based on available study hours
- **Video Resource Curation**: Automatically searches and recommends relevant YouTube tutorials for challenging topics
- **Professional Reporting**: Produces both Markdown and JSON formatted reports with comprehensive study plans
- **Smart File Detection**: Uses magic byte detection to accurately identify file types regardless of extensions

## Prerequisites

- Kestra v0.10.0 or higher installed and running
- Docker configured for Kestra task runners
- Required API credentials:
  - **HuggingFace API Key**: For AI-powered content analysis (required)
  - **SerpAPI Key**: For YouTube video search functionality (required)
- Google Drive folder with publicly accessible study materials
  - Folder must be set to "Anyone with the link can view"
  - Individual files within the folder must also be shared publicly

## Installation

### Setting Up Kestra

Ensure Kestra is properly installed and accessible on your system. For detailed installation instructions, refer to the [official Kestra documentation](https://kestra.io/docs).

**Quick Setup:**
```bash
docker run -d --name kestra \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  kestra/kestra:latest
```

Access the Kestra UI at `http://localhost:8080`

### Workflow Deployment

1. Navigate to the Kestra web interface at `http://localhost:8080`
2. Go to **Flows** → **Create**
3. Set the namespace as `company.team` and flow ID as `Study_Helper`
4. Copy the contents of `company.team.Study_Helper.yaml`
5. Paste the configuration into the flow editor
6. Click **Save** to deploy the workflow

## Usage

### Preparing Your Study Materials

1. Upload your study materials (PDF, DOCX, or TXT files) to a Google Drive folder
2. Right-click the folder → **Share** → Set to "Anyone with the link can view"
3. **Important**: Select all files in the folder, right-click → **Share** → Set each file to "Anyone with the link can view"
4. Copy the folder URL or folder ID

### Executing the Workflow

1. Access the Kestra web interface
2. Navigate to **Flows** → `company.team` → `Study_Helper`
3. Click **Execute**
4. Provide the following inputs:

   | Input | Description | Example |
   |-------|-------------|---------|
   | `drive_folder_url` | Google Drive folder URL or ID | `https://drive.google.com/drive/folders/1ABC...` |
   | `huggingface_api_key` | Your HuggingFace API token | `hf_...` |
   | `serpapi_api_key` | Your SerpAPI key for video search | `abc123...` |
   | `user_study_hours_per_day` | Daily study time available | `2.5` |

5. Click **Execute** to start the workflow
6. Monitor real-time progress in the execution logs

### Output Files

Upon successful completion, the workflow generates two comprehensive reports:

**1. `study_report.md`** - Formatted Markdown Report
- Executive summary with difficulty assessment
- Comprehensive topic breakdown
- Day-by-day study schedule with activities and learning objectives
- Curated video resources (for difficult topics)
- Study tips and best practices

**2. `study_report.json`** - Structured JSON Data
- Machine-readable format for integration with other tools
- Complete metadata including timestamps and processing details
- Hierarchical organization of analysis results and study plans

**Output Structure:**
```json
{
  "metadata": {
    "generated_at": "ISO timestamp",
    "status": "success",
    "files_processed": 3
  },
  "analysis": {
    "summary": "Content overview",
    "difficulty": "TOUGH/SIMPLE",
    "topics": [...],
    "key_concepts": [...]
  },
  "study_plan": {
    "schedule": [...]
  },
  "video_resources": [...]
}
```

### Downloading Reports

1. Navigate to the execution details page
2. Click on the **Outputs** tab
3. Download `study_report.md` and `study_report.json` from the output files section

## Workflow Architecture

Study Helper implements a sophisticated six-stage pipeline for intelligent study material processing:

### Task 1: Content Extraction (`fetch_drive_folder`)
- Retrieves files from Google Drive using folder ID extraction
- Implements magic byte detection for accurate file type identification
- Supports PDF (PyPDF2), DOCX (python-docx), and plain text formats
- Handles up to 15 files per execution with content validation
- **Output**: `study_content.txt` containing extracted text from all documents

### Task 2: AI Analysis (`ai_comprehensive_analysis`)
- Processes extracted content using HuggingFace SmolLM3-3B model
- Analyzes content to determine difficulty level (TOUGH/SIMPLE)
- Identifies primary topics, key concepts, and prerequisites
- Estimates total study hours required
- **Output**: `ai_analysis_result.txt` with structured JSON analysis

### Task 3: JSON Parsing (`parse_analysis`)
- Extracts and validates structured data from AI response
- Implements fallback mechanisms for parsing errors
- Normalizes topics, concepts, and difficulty assessments
- **Output**: Structured variables for downstream tasks

### Task 4: Study Plan Generation (`generate_study_plan`)
- Creates personalized day-by-day study schedules using AI
- Calculates study timeline based on available daily hours
- Assigns progressive learning objectives for each day
- Generates actionable activities and milestones
- **Output**: Detailed study schedule with dates and activities

### Task 5: Video Resource Curation (`check_difficulty`)
- Conditionally executes when difficulty is marked as "TOUGH"
- Searches YouTube via SerpAPI for top 3 topics
- Retrieves video metadata: title, channel, duration, and links
- **Output**: Curated list of educational video resources

### Task 6: Report Assembly (`assemble_final_output`)
- Aggregates all analysis results and study plans
- Generates professional Markdown report with formatted sections
- Creates structured JSON export for programmatic access
- Produces clean console summary with key metrics
- **Output**: `study_report.md` and `study_report.json`

### Data Flow
```
Google Drive → Content Extraction → AI Analysis → JSON Parsing
                                                       ↓
                                              Study Plan Generation
                                                       ↓
                        Video Curation ← Difficulty Check
                                    ↓
                            Report Assembly
                                    ↓
                        Markdown + JSON Reports
```

## Troubleshooting

### Common Issues

#### No files found in Google Drive folder
**Error Message**: `"No files found in folder"`

**Solution**:
1. Verify the folder URL/ID is correct
2. Ensure folder is set to "Anyone with the link can view"
3. **Critical**: Right-click each file → Share → "Anyone with the link can view"
4. Wait 1-2 minutes after changing permissions before re-executing

#### File content appears corrupted or binary
**Symptoms**: Output shows `PK` or unreadable characters

**Cause**: File type detection failure or unsupported format

**Solution**:
- Ensure files are valid PDF, DOCX, or TXT formats
- Check that files are not password-protected
- Verify files are not corrupted (test opening locally)
- The workflow now uses magic byte detection to prevent this issue

#### API authentication failures
**Error Message**: `401 Unauthorized` or `403 Forbidden`

**Solution**:
- Verify HuggingFace API key is valid: https://huggingface.co/settings/tokens
- Verify SerpAPI key is active: https://serpapi.com/manage-api-key
- Check API key format (no extra spaces or quotes)
- Ensure API quotas are not exceeded

#### Workflow timeout or hangs
**Symptoms**: Task appears stuck or exceeds expected duration

**Solution**:
- Check Docker container resources (CPU/Memory)
- Reduce number of files in Google Drive folder (max 15 recommended)
- Verify network connectivity to external APIs
- Review Kestra worker logs: `docker logs kestra`

#### Empty or incomplete study plan
**Symptoms**: Study plan has minimal details or missing sections

**Cause**: AI model returned unparseable response

**Solution**:
- The workflow includes fallback mechanisms for AI failures
- Check `ai_analysis_result.txt` in outputs for raw AI response
- Verify content file has sufficient material (minimum 100 characters)
- Try re-executing the workflow (AI responses can vary)

#### Video recommendations not appearing
**Expected Behavior**: Videos only appear when difficulty is "TOUGH"

**Verification**:
- Check the difficulty assessment in the output logs
- Ensure SerpAPI key is configured correctly
- Video search is intentionally skipped for "SIMPLE" content

### Debugging Steps

1. **Check Execution Logs**:
   - Navigate to execution details in Kestra UI
   - Review each task's logs sequentially
   - Look for error messages or warnings

2. **Verify Output Files**:
   - Check if `study_content.txt` was generated (Task 1)
   - Verify `ai_analysis_result.txt` exists (Task 2)
   - Confirm final reports were created (Task 6)

3. **Test API Connectivity**:
   ```bash
   # Test HuggingFace API
   curl -H "Authorization: Bearer YOUR_HF_KEY" \
     https://router.huggingface.co/v1/models
   
   # Test SerpAPI
   curl "https://serpapi.com/search?engine=youtube&q=test&api_key=YOUR_KEY"
   ```

4. **Review Docker Logs**:
   ```bash
   docker logs kestra --tail 100
   ```

## Advanced Configuration

### Customizing AI Models

The workflow uses HuggingFace's SmolLM3-3B model by default. To use alternative models:

1. Modify the `model` parameter in Task 2 and Task 4:
   ```yaml
   payload = {
       "model": "your-preferred-model",  # Change this
       "messages": [{"role": "user", "content": prompt}],
       "max_tokens": 1000
   }
   ```

2. Supported models must be available through HuggingFace Inference API

### Adjusting File Processing Limits

To process more than 15 files, modify Task 1:
```yaml
for idx, file_id in enumerate(potential_ids[:15], 1):  # Change 15 to desired limit
```

**Note**: Processing more files increases execution time and resource consumption.

### Customizing Study Plan Format

Modify the JSON template in Task 4 to adjust study plan structure:
```python
plan_template = [
  {
    "day": 1,
    "topic": "topic name",
    "duration_hours": 2.0,
    "activities": ["activity1", "activity2"],
    "learning_objective": "what to achieve",
    "custom_field": "your_value"  # Add custom fields
  }
]
```

## Performance Optimization

### Recommended Resources

- **Minimum**: 2 CPU cores, 4GB RAM
- **Recommended**: 4 CPU cores, 8GB RAM
- **Storage**: 10GB free space for Docker images and temporary files

### Execution Time Estimates

| Files | Size (Total) | Estimated Duration |
|-------|-------------|-------------------|
| 1-3   | < 5MB      | 2-3 minutes       |
| 4-8   | 5-15MB     | 4-6 minutes       |
| 9-15  | 15-30MB    | 7-10 minutes      |

*Times vary based on API response times and system resources*

## Security Considerations

- **API Keys**: Store credentials securely using Kestra's secret management
- **Google Drive**: Only share files necessary for analysis; avoid sensitive documents
- **Data Privacy**: All processing occurs within your Kestra instance; content is not permanently stored
- **Network**: Ensure secure connections to external APIs (HTTPS enforced)

## Contributing

We welcome contributions to improve Study Helper! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Test your changes thoroughly with various file types and scenarios
4. Ensure all tasks execute successfully
5. Update documentation to reflect changes
6. Submit a pull request with detailed description

**Areas for Contribution**:
- Additional file format support (PPTX, Markdown, etc.)
- Alternative AI model integrations
- Enhanced error handling and recovery mechanisms
- Internationalization and multi-language support
- Performance optimizations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

### Documentation Resources
- [Kestra Documentation](https://kestra.io/docs) - Workflow platform reference
- [HuggingFace API](https://huggingface.co/docs/api-inference) - AI model documentation
- [SerpAPI Documentation](https://serpapi.com/docs) - Video search API reference

### Community Support
- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join the conversation in GitHub Discussions
- **Kestra Community**: [Slack Channel](https://kestra.io/slack) for platform-specific questions

### Professional Support
For enterprise deployments or custom implementations, consider reaching out for professional consulting services.

## Acknowledgments

Study Helper is built with the following open-source technologies:

- **[Kestra](https://kestra.io)** - Workflow orchestration platform
- **[HuggingFace](https://huggingface.co)** - AI model hosting and inference
- **[SerpAPI](https://serpapi.com)** - YouTube search functionality
- **[PyPDF2](https://pypdf2.readthedocs.io)** - PDF text extraction
- **[python-docx](https://python-docx.readthedocs.io)** - Microsoft Word document processing
- **[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)** - HTML parsing

Special thanks to the open-source community for making this project possible.

---

**Made with ❤️ for students everywhere**
