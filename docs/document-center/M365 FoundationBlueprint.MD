RAE M365 Foundation Audit Blueprint
Version: 1.0 Status: Proposed Owner: RAE Digital Transformation
________________________________________
Objective
เปลี่ยนแนวทางจาก
WTMS → OneDrive → Custom Registry
ไปสู่
WTMS → Microsoft 365 Platform → RAE Portal
โดยใช้เครื่องมือที่มหาวิทยาลัยมีอยู่แล้วให้มากที่สุด
________________________________________
Strategic Principle
Build Less. Govern More.
Website should not become a document management system.
Microsoft 365 should become the document management platform.
RAE Website should become the public experience layer.
________________________________________
Target Architecture
WTMS Legacy ↓ Migration ↓ SharePoint Online ↓ Microsoft Lists ↓ Power Automate ↓ Graph API / Export Layer ↓ RAE Public Portal (Next.js)
________________________________________
Success Criteria
•	No primary documents stored on VPS
•	No manual registry maintenance
•	Metadata managed inside M365
•	Approval workflow integrated
•	Searchable document catalog
•	Public website remains stateless
•	Governance enforced by platform
________________________________________
Phase M365-1
License & Capability Audit
Objective: Identify available Microsoft 365 services.
Audit Checklist:
•	SharePoint Online
•	Microsoft Lists
•	Power Automate
•	Teams Approvals
•	Microsoft Forms
•	Power BI
•	Microsoft Graph API
•	Azure App Registration access
•	Copilot availability
Deliverable:
M365_LICENSE_AUDIT.md
Decision:
AVAILABLE LIMITED NOT AVAILABLE
per service
________________________________________
Phase M365-2
Information Architecture Design
Objective:
Design long-term document structure.
Document Categories:
•	งานบริหารและธุรการ
•	งานคลังและพัสดุ
•	งานวิจัย
•	งานบริการวิชาการ
•	งานนโยบายและแผน
•	คู่มือปฏิบัติงาน
Future Categories:
•	Green Office
•	Research Portal
•	Learning Center
•	Quality Assurance
Deliverables:
taxonomy.v2.json information-architecture.md
________________________________________
Phase M365-3
SharePoint Foundation
Objective:
Create official storage layer.
Create Site:
RAE Document Center
Create Document Libraries:
•	Administration
•	FinanceProcurement
•	Research
•	AcademicServices
•	PlanningPolicy
•	SOPManuals
Metadata Columns:
•	Document ID
•	Title
•	Category
•	Owner
•	Status
•	Version
•	Updated Date
•	Tags
•	Public Visibility
Deliverables:
sharepoint-site-design.md library-schema.md
________________________________________
Phase M365-4
Microsoft Lists Registry
Objective:
Create authoritative metadata registry.
List Name:
RAE Document Registry
Required Fields:
•	DocumentID
•	Title
•	Category
•	Owner
•	Status
•	FileURL
•	Version
•	UpdatedDate
•	Tags
•	Notes
Benefits:
•	Search
•	Filtering
•	Reporting
•	Governance
Deliverables:
registry-list-schema.md
________________________________________
Phase M365-5
Power Automate Governance
Objective:
Automate document lifecycle.
Workflow A:
Document Upload
File Uploaded ↓ Metadata Validation ↓ Registry Update ↓ Owner Notification
Workflow B:
Document Approval
Draft ↓ Review ↓ Approve ↓ Publish
Workflow C:
Archive Control
Expired ↓ Review ↓ Archive
Deliverables:
power-automate-flows.md
________________________________________
Phase M365-6
Teams Integration
Objective:
Operational governance.
Create Team:
RAE Document Governance
Channels:
•	New Documents
•	Reviews
•	Approvals
•	Archive Requests
Notifications:
•	Missing Metadata
•	Approval Requests
•	Expiring Documents
Deliverables:
teams-governance.md
________________________________________
Phase M365-7
Migration Pilot
Objective:
Validate migration process.
Scope:
10–20 representative documents
Activities:
•	Upload
•	Metadata assignment
•	Registry synchronization
•	Approval workflow test
•	Public access validation
Success Criteria:
•	No broken links
•	Metadata complete
•	Approval flow working
Deliverables:
pilot-migration-report.md
________________________________________
Phase M365-8
Public Portal Integration
Objective:
Expose documents to users.
Portal Responsibilities:
•	Search
•	Browse
•	Category Filter
•	Download
•	Public Metadata
Portal Must Not:
•	Store master files
•	Manage approval workflows
•	Maintain authoritative metadata
Integration Options:
Option A: Microsoft Graph API
Option B: Scheduled Registry Export JSON
Preferred:
Registry Export JSON (for static hosting simplicity)
Deliverables:
integration-architecture.md
________________________________________
Phase M365-9
Analytics & Compliance
Objective:
Governance visibility.
Dashboards:
•	Documents by Category
•	Documents by Owner
•	Expiring Documents
•	Missing Metadata
•	Approval SLA
Tools:
•	Power BI
•	Microsoft Lists Views
Deliverables:
document-governance-dashboard.md
________________________________________
Migration Strategy
Current Direction:
WTMS ↓ Custom Registry ↓ OneDrive
New Direction:
WTMS ↓ SharePoint ↓ Microsoft Lists ↓ Power Automate ↓ Portal
Result:
Less custom code Lower maintenance Better governance Higher sustainability
________________________________________
Long-Term Vision
Single M365 Document Platform
Serving:
•	RAE
•	Green Office
•	Research Portal
•	Learning Center
With one governance model.
Website becomes presentation.
Microsoft 365 becomes source of truth.