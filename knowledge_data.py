SKILLS = """
programming|Programming Fundamentals|Foundations||CLI task manager with tests
math_foundations|Discrete Math & Linear Algebra|Foundations||Linear algebra + discrete math problem set
probability|Probability & Statistics|Foundations|math_foundations|A/B test analysis notebook
git|Git & Collaboration|Foundations|programming|Contribute 3 PRs to an open-source repo
linux|Linux & Shell|Foundations||Script a VPS setup end to end
data_structures|Data Structures|Foundations|programming|Implement hash map, heap and trie from scratch
algorithms|Algorithms|Foundations|data_structures,math_foundations|Pathfinding visualiser (A*, Dijkstra)
oop|OOP & Design Patterns|Foundations|programming|Refactor a project using five design patterns
testing|Testing & TDD|Foundations|programming|Add CI with 80% coverage to an existing project
networking|Computer Networking|Foundations||HTTP server on raw sockets
os_concepts|Operating Systems|Foundations|programming,linux|Toy shell with pipes and job control
databases|Databases & SQL|Foundations|programming|Blog API with Postgres, indexes, migrations
python|Python|Languages|programming|Packaged Python tool that automates a real task
javascript|JavaScript|Languages|programming|Interactive browser game without frameworks
typescript|TypeScript|Languages|javascript|Port a JS project to strict TypeScript
java|Java|Languages|oop|Spring Boot REST service
cpp|C / C++|Languages|data_structures,os_concepts|Custom memory allocator with unit tests
rust|Rust|Languages|cpp|CLI tool with safe concurrency
go|Go|Languages|programming|Concurrent web crawler
html_css|HTML & CSS|Web||Responsive multi-page site
frontend_fw|Frontend Frameworks (React/Vue)|Web|javascript,html_css|SPA with routing and state management
node_backend|Backend Frameworks & REST|Web|programming,databases,networking|REST API with auth and pagination
api_design|API Design (REST/GraphQL)|Web|node_backend|Versioned public API with OpenAPI docs
auth|Authentication & Authorization|Web|node_backend|OAuth2/JWT login system with role-based access
mobile_android|Android (Kotlin)|Mobile|oop|Offline-first notes app
mobile_ios|iOS (Swift)|Mobile|oop|Habit tracker in SwiftUI
cross_platform|Cross-platform (Flutter/React Native)|Mobile|oop|One app shipped on iOS and Android
mobile_arch|Mobile Architecture & Release|Mobile|oop,testing|Modularise an app with MVVM and publish to a store
containers|Docker & Containers|Infrastructure|linux|Containerise a multi-service app
cloud|Cloud Platforms (AWS/GCP/Azure)|Infrastructure|linux,networking|Deploy a 3-tier app on a public cloud
iac|Infrastructure as Code|Infrastructure|cloud|Terraform a full environment from scratch
cicd|CI/CD Pipelines|Infrastructure|git,containers|Pipeline: test, build, deploy, rollback
kubernetes|Kubernetes|Infrastructure|containers,networking|Run a multi-service app on a k8s cluster
monitoring|Observability & Monitoring|Infrastructure|linux|Metrics, logs and alerting dashboard
sre_practices|SRE & Incident Management|Infrastructure|monitoring,cloud|Define SLOs and run a game-day exercise
system_design|System Design|Infrastructure|databases,networking,algorithms|URL shortener with cache, queue and load test
distributed|Distributed Systems|Infrastructure|system_design,os_concepts|Replicated key-value store with consensus
security_fundamentals|Security Fundamentals|Security|networking,linux|Harden a server and write a threat model
pentest|Penetration Testing|Security|security_fundamentals|Pentest report on an intentionally vulnerable app
web_security|Web Application Security (OWASP)|Security|security_fundamentals,node_backend|Find and fix OWASP Top 10 flaws in your own app
crypto|Applied Cryptography|Security|math_foundations,security_fundamentals|Implement and attack a toy cipher scheme
incident_response|Incident Response & Forensics|Security|security_fundamentals,os_concepts|Forensic write-up of a disk image
malware_re|Reverse Engineering & Malware Analysis|Security|os_concepts,cpp,security_fundamentals|Analyse a sample in a sandbox
cloud_security|Cloud Security|Security|cloud,security_fundamentals|Audit and harden a cloud account
pandas_analysis|Data Analysis (Pandas/SQL)|Data & AI|python,probability|Exploratory analysis of a public dataset
data_viz|Data Visualisation & BI|Data & AI|pandas_analysis|Interactive stakeholder dashboard
experiment|Experimentation & Causal Inference|Data & AI|probability|Design and analyse an A/B test
ml|Machine Learning|Data & AI|python,probability,math_foundations|End-to-end project with proper validation
deep_learning|Deep Learning|Data & AI|ml|Train a CNN or transformer from scratch
nlp|Natural Language Processing|Data & AI|deep_learning|Text classifier plus semantic search
cv|Computer Vision|Data & AI|deep_learning|Object detector deployed on an edge device
llm_apps|LLM Application Engineering|Data & AI|python,api_design|RAG assistant with an evaluation harness
mlops|MLOps|Data & AI|ml,containers,cicd|Training + serving pipeline with monitoring
data_eng|Data Pipelines (ETL/ELT)|Data & AI|databases,python|Scheduled ETL pipeline with Airflow
big_data|Big Data (Spark/Kafka)|Data & AI|data_eng|Streaming pipeline with Kafka and Spark
warehousing|Data Warehousing & Modelling|Data & AI|databases|Dimensional model in a cloud warehouse
game_engine|Game Engine (Unity/Unreal)|Game & Graphics|oop|Playable 3D vertical slice
graphics|Computer Graphics|Game & Graphics|math_foundations,cpp|Software ray tracer
ar_vr|AR/VR Development|Game & Graphics|game_engine,graphics|Hand-tracked VR prototype
embedded_c|Embedded C|Embedded & IoT|programming,os_concepts|Sensor-to-UART firmware on a dev board
hardware_interfaces|Hardware Interfaces (I2C/SPI/UART)|Embedded & IoT|embedded_c|Multi-sensor data logger
rtos|RTOS & Firmware Design|Embedded & IoT|embedded_c|Multitasking firmware on FreeRTOS
iot|IoT & Edge Systems|Embedded & IoT|networking,embedded_c|Sensor network reporting to the cloud
test_automation|Test Automation|Quality|testing,programming|End-to-end suite in Playwright with CI
perf_testing|Performance & Load Testing|Quality|testing,networking|Load-test an API and fix bottlenecks
blockchain|Blockchain & Smart Contracts|Emerging|data_structures,networking|Audited ERC-20 contract plus dApp
compilers|Compilers & Language Design|Emerging|algorithms,data_structures|Interpreter for a small language
communication|Communication & Teamwork|Professional||Write and present a design RFC
agile|Agile & Project Management|Professional|communication|Run a two-sprint team project
"""

CAREERS = """
Backend Engineer|Software Engineering|Web & APIs|programming:4:5,data_structures:4:4,databases:4:5,node_backend:4:5,api_design:3:4,system_design:3:4,testing:3:3,git:3:3,networking:3:3
Frontend Engineer|Software Engineering|Web & APIs|javascript:4:5,html_css:4:5,frontend_fw:4:5,testing:3:3,git:3:3,api_design:2:2,communication:3:2
Full-Stack Engineer|Software Engineering|Web & APIs|javascript:4:4,frontend_fw:4:4,node_backend:4:4,databases:3:4,auth:3:3,git:3:3,testing:3:3
Android Engineer|Software Engineering|Mobile|mobile_android:4:5,oop:4:4,mobile_arch:3:4,api_design:3:3,testing:3:3,git:3:2
iOS Engineer|Software Engineering|Mobile|mobile_ios:4:5,oop:4:4,mobile_arch:3:4,api_design:3:3,testing:3:3,git:3:2
Cross-Platform Mobile Engineer|Software Engineering|Mobile|cross_platform:4:5,mobile_arch:3:4,javascript:3:3,api_design:3:3,testing:3:3
Systems Programmer|Software Engineering|Systems|cpp:4:5,os_concepts:4:5,algorithms:4:4,data_structures:4:4,rust:3:3,networking:3:3,linux:3:3
Compiler Engineer|Software Engineering|Systems|compilers:4:5,cpp:4:4,algorithms:4:4,data_structures:4:3,os_concepts:3:3
Distributed Systems Engineer|Software Engineering|Systems|distributed:4:5,system_design:4:5,go:3:3,databases:4:4,networking:4:3,algorithms:3:3
Data Analyst|Data & AI|Analytics|pandas_analysis:4:5,databases:4:4,data_viz:4:5,probability:3:4,communication:3:3
Data Scientist|Data & AI|Machine Learning|python:4:4,probability:4:5,ml:4:5,pandas_analysis:4:4,experiment:3:4,data_viz:3:3,communication:3:3
ML Engineer|Data & AI|Machine Learning|python:4:5,ml:4:5,deep_learning:3:4,mlops:3:4,math_foundations:4:4,algorithms:3:3,testing:3:2
AI Research Engineer|Data & AI|Machine Learning|deep_learning:4:5,math_foundations:4:5,probability:4:4,python:4:4,nlp:3:2,cv:3:2
NLP / LLM Engineer|Data & AI|Generative AI|nlp:4:5,deep_learning:3:4,python:4:5,llm_apps:4:5,mlops:3:3
AI Application Developer|Data & AI|Generative AI|llm_apps:4:5,python:4:4,api_design:3:4,node_backend:3:3
Computer Vision Engineer|Data & AI|Machine Learning|cv:4:5,deep_learning:4:5,python:4:4,math_foundations:4:4,cpp:3:2
MLOps Engineer|Data & AI|Data Platforms|mlops:4:5,containers:4:4,cicd:4:4,cloud:3:4,python:3:3,monitoring:3:3
Data Engineer|Data & AI|Data Platforms|data_eng:4:5,databases:4:5,python:4:4,big_data:3:4,warehousing:3:4,cloud:3:3
DevOps Engineer|Infrastructure & Cloud|DevOps|linux:4:5,containers:4:5,cicd:4:5,iac:3:4,cloud:3:4,monitoring:3:3,git:3:3
Cloud Engineer|Infrastructure & Cloud|Cloud|cloud:4:5,networking:4:4,iac:4:4,linux:3:3,security_fundamentals:3:3
Site Reliability Engineer|Infrastructure & Cloud|Reliability|sre_practices:4:5,monitoring:4:5,linux:4:4,kubernetes:3:4,distributed:3:3,programming:3:3
Platform Engineer|Infrastructure & Cloud|DevOps|kubernetes:4:5,iac:4:4,cicd:4:4,cloud:4:4,go:3:3
Network Engineer|Infrastructure & Cloud|Networking|networking:5:5,linux:3:3,security_fundamentals:3:3,cloud:2:2
Database Administrator|Infrastructure & Cloud|Databases|databases:5:5,linux:3:3,monitoring:3:3,os_concepts:2:2
Security Engineer|Security|Defensive|security_fundamentals:4:5,networking:4:4,linux:4:4,programming:3:4,web_security:3:3,cloud_security:3:2
Penetration Tester|Security|Offensive|pentest:4:5,security_fundamentals:4:5,networking:4:4,web_security:3:4,linux:4:3,programming:3:2
Incident Responder|Security|Defensive|incident_response:4:5,security_fundamentals:4:5,os_concepts:3:3,networking:3:3,monitoring:3:3
Application Security Engineer|Security|Application|web_security:4:5,auth:4:4,security_fundamentals:3:4,programming:4:3,testing:3:2
Cryptography Engineer|Security|Cryptography|crypto:4:5,math_foundations:4:5,algorithms:3:3,security_fundamentals:3:3,cpp:3:2
Malware Analyst|Security|Offensive|malware_re:4:5,os_concepts:4:4,cpp:4:3,security_fundamentals:3:3
Cloud Security Engineer|Security|Defensive|cloud_security:4:5,cloud:4:4,security_fundamentals:4:4,iac:3:3
Game Developer|Game & Graphics|Gameplay|game_engine:4:5,cpp:4:4,oop:4:4,graphics:3:4,algorithms:3:3,math_foundations:3:3
Graphics Engineer|Game & Graphics|Rendering|graphics:4:5,cpp:4:5,math_foundations:4:5,algorithms:3:3,game_engine:3:2
AR/VR Developer|Game & Graphics|Immersive|ar_vr:4:5,game_engine:4:4,graphics:3:3,math_foundations:3:3,oop:3:3
Embedded Engineer|Embedded & IoT|Firmware|embedded_c:4:5,rtos:3:4,hardware_interfaces:4:4,os_concepts:3:3,cpp:3:2
IoT Engineer|Embedded & IoT|Connected Devices|iot:4:5,embedded_c:3:4,networking:3:4,cloud:3:3,hardware_interfaces:3:3
QA Automation Engineer|Quality Engineering|Automation|test_automation:4:5,testing:4:5,programming:3:4,cicd:3:3,perf_testing:3:2
Performance Engineer|Quality Engineering|Performance|perf_testing:4:5,monitoring:3:4,networking:3:3,system_design:3:3,programming:3:3
Blockchain Developer|Emerging Tech|Web3|blockchain:4:5,crypto:3:4,javascript:3:3,data_structures:3:3,security_fundamentals:3:3
"""

SKILLS += """
design_fundamentals|Visual Design Fundamentals|Design||Redesign a real app screen with a written rationale
figma|UI Design & Prototyping (Figma)|Design|design_fundamentals|Clickable prototype of a 6-screen app
ux_research|UX Research|Design||Run 5 user interviews and a usability-test report
interaction_design|Interaction & Motion Design|Design|figma|Animated micro-interaction prototype
design_systems|Design Systems|Design|figma|Component library with design tokens
mobile_ui|Mobile UI Patterns|Design|figma|iOS and Android versions of one app design
accessibility|Accessibility (WCAG)|Design|html_css|Audit and fix a site to WCAG AA
cms|CMS & No-code Web|Web|html_css|Build and customise a CMS-based business site
web_perf|Web Performance|Web|frontend_fw|Halve a site's load time, proven with Lighthouse
software_architecture|Software Architecture|Infrastructure|system_design,oop|Architecture decision records for a real system
robotics|Robotics & ROS|Embedded & IoT|cpp,python|Autonomous line-following robot in ROS
bioinformatics|Bioinformatics|Data & AI|python,pandas_analysis|Variant-calling pipeline on public genomes
game_design|Game Design|Game & Graphics||Paper prototype plus one playtested level
prod_mgmt|Product Management|Professional|communication|PRD and roadmap for a feature
tech_writing|Technical Writing|Professional|communication|Docs site for an open-source tool
"""

CAREERS += """
UI/UX Designer|Design & Product|UI/UX|design_fundamentals:4:5,figma:4:5,ux_research:3:4,interaction_design:3:3,design_systems:3:3,accessibility:3:3,communication:3:3
Web Designer|Design & Product|Web Design|design_fundamentals:4:5,html_css:4:5,figma:3:4,cms:3:3,accessibility:3:3,javascript:2:2
Mobile App Designer|Design & Product|Mobile Design|mobile_ui:4:5,figma:4:5,design_fundamentals:4:4,ux_research:3:3,interaction_design:3:3
Product Designer|Design & Product|Product Design|ux_research:4:5,figma:4:5,design_systems:4:4,design_fundamentals:4:4,prod_mgmt:3:3,communication:4:3
Design Engineer|Design & Product|Design Engineering|frontend_fw:4:5,design_systems:4:4,html_css:4:4,interaction_design:3:4,accessibility:3:3,figma:3:2
Accessibility Specialist|Design & Product|Accessibility|accessibility:4:5,html_css:4:4,ux_research:3:3,testing:3:2
Technical Product Manager|Design & Product|Product Management|prod_mgmt:4:5,communication:4:4,agile:4:4,system_design:2:3,ux_research:2:2
Technical Writer|Design & Product|Documentation|tech_writing:4:5,communication:4:4,programming:2:3,git:3:2,api_design:2:2
Developer Advocate|Design & Product|Developer Relations|communication:4:5,tech_writing:3:4,programming:4:4,api_design:3:3,cloud:2:2
Software Architect|Software Engineering|Architecture|software_architecture:4:5,system_design:4:5,oop:4:4,distributed:3:3,databases:4:3,communication:4:3
Web Performance Engineer|Software Engineering|Web & APIs|web_perf:4:5,frontend_fw:4:4,networking:3:3,perf_testing:3:3,monitoring:3:2
Java Backend Engineer|Software Engineering|Web & APIs|java:4:5,databases:4:4,node_backend:4:4,api_design:3:3,system_design:3:3,testing:3:3
Go Cloud-Native Developer|Software Engineering|Web & APIs|go:4:5,databases:4:4,api_design:3:4,containers:3:4,kubernetes:3:3,system_design:3:3
Python Developer|Software Engineering|Web & APIs|python:4:5,node_backend:3:4,databases:3:4,testing:3:3,git:3:3,api_design:3:3
Robotics Engineer|Embedded & IoT|Robotics|robotics:4:5,cpp:4:4,python:3:3,math_foundations:4:4,embedded_c:3:3,algorithms:3:3
Bioinformatics Engineer|Data & AI|Scientific Computing|bioinformatics:4:5,python:4:4,pandas_analysis:3:4,probability:3:3,ml:3:3
Game Designer|Game & Graphics|Game Design|game_design:4:5,game_engine:3:4,communication:3:3,design_fundamentals:3:3,programming:2:2
Data Architect|Data & AI|Data Platforms|warehousing:4:5,data_eng:4:4,databases:5:4,cloud:3:3,system_design:3:3
BI Developer|Data & AI|Analytics|data_viz:4:5,databases:4:5,warehousing:3:4,pandas_analysis:3:3
Cloud Solutions Architect|Infrastructure & Cloud|Cloud|cloud:4:5,system_design:4:4,networking:3:3,security_fundamentals:3:3,communication:4:3
"""

ALIASES = {
 "Frontend Engineer": ["frontend developer", "front end developer", "front-end developer", "web developer", "react developer", "ui developer"],
 "Backend Engineer": ["backend developer", "back end developer", "back-end developer", "server developer", "api developer"],
 "Full-Stack Engineer": ["full stack developer", "fullstack developer", "full-stack developer"],
 "Android Engineer": ["android developer", "kotlin developer"],
 "iOS Engineer": ["ios developer", "swift developer", "iphone developer"],
 "Cross-Platform Mobile Engineer": ["flutter developer", "react native developer", "mobile developer", "app developer"],
 "Game Developer": ["game dev", "unity developer", "unreal developer"],
 "ML Engineer": ["machine learning engineer", "machine learning developer"],
 "Data Scientist": ["ds", "data science"],
 "AI Research Engineer": ["ai researcher", "research scientist"],
 "NLP / LLM Engineer": ["llm engineer", "nlp engineer", "generative ai engineer"],
 "DevOps Engineer": ["devops", "build engineer"],
 "Site Reliability Engineer": ["sre"],
 "Security Engineer": ["cybersecurity engineer", "cyber security", "infosec"],
 "Penetration Tester": ["pentester", "ethical hacker"],
 "QA Automation Engineer": ["sdet", "qa engineer", "test engineer", "tester"],
 "Embedded Engineer": ["firmware engineer", "embedded developer"],
 "UI/UX Designer": ["ui designer", "ux designer", "web designer", "app designer", "user experience designer", "interface designer"],
 "Web Designer": ["website designer", "web design", "landing page designer"],
 "Mobile App Designer": ["app designer", "mobile designer", "mobile ui designer"],
 "Product Designer": ["product design"],
 "Design Engineer": ["creative technologist", "design technologist"],
 "Technical Product Manager": ["product manager", "pm", "tpm"],
 "Software Architect": ["solution architect", "software architecture"],
 "Cloud Solutions Architect": ["solutions architect", "aws architect"],
 "Data Analyst": ["analyst", "business analyst"],
 "Python Developer": ["django developer", "flask developer"],
}
