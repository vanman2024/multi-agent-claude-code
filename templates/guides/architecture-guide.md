# Architecture Document Guide

## Required Sections to Include

### 1. Project Information
- Project Name
- Project Type (api/fullstack/frontend/integration)
- Architecture Version
- Decision Date

### 2. Core Technology Stack (adapt to project type)

For **API Projects**:
- Backend Framework (FastAPI, Express, etc.)
- API Protocol (REST, GraphQL, WebSocket)
- External Services Integration
- NO Database section (using external data sources)

For **Full-Stack Projects**:
- Frontend Framework
- Backend Framework  
- Database
- State Management

For **Integration Projects**:
- Source Systems
- Target Systems
- Middleware/Orchestration
- Data Transformation

### 3. Key Design Decisions

Include WHY you chose each technology:
- What alternatives were considered
- Why this choice fits the project
- Trade-offs accepted

### 4. Project Structure

Show the actual folder structure:
```
project-root/
├── [relevant folders for project type]
```

### 5. API Design (if applicable)
- Endpoint patterns
- Authentication method
- Error handling
- Rate limiting

### 6. Non-Negotiable Rules
List constraints that CANNOT change:
- Port numbers
- Core frameworks
- File organization

### 7. Decision Log
Track major architecture decisions with dates

## Questions to Answer

1. What type of project is this?
2. What are the core technologies?
3. Why were they chosen?
4. What patterns will we follow?
5. What are the constraints?
6. How is the code organized?

## Project Type Variations

### API-Only
- Focus on endpoints and integrations
- External data sources
- Webhook handling
- No UI components

### Full-Stack
- Complete architecture
- All layers documented
- Database design included

### Integration/Webhook
- System connections
- Data flow diagrams
- Transformation logic
- Error recovery