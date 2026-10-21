# Verba — Project Specification

## 1. Project Overview

**Verba** is a personal language-learning web application designed to help users collect, organize, review, and reuse language patterns, collocations, verb-preposition combinations, grammatical structures, and practical expressions.

The primary goal of Verba is to help language learners improve their ability to actively produce a language by maintaining a searchable, structured library of useful language patterns.

Verba is initially intended for personal German learning, but its data model and architecture should be flexible enough to support other languages in the future.

Verba is not intended to be another traditional flashcard application. Its main purpose is to provide a persistent reference library that users can access while writing, speaking, studying, or practicing a language.

## 2. The Problem Verba Solves

Language learners encounter useful structures through several activities:

- Writing longer texts and correcting them with AI.

- Creating sentences using specific vocabulary items.

- Practicing conversations with AI.

- Reading and listening to native-language content.

- Reviewing grammatical explanations and corrections.

These activities continuously introduce new language patterns and reveal recurring mistakes.

Traditional spaced-repetition systems, such as Anki, are useful for long-term memorization but do not always provide convenient access to every learned structure at the exact moment it is needed.

A learner may know that a particular verb requires a specific preposition but forget the combination while writing a sentence. The structure may exist in a flashcard deck but may not appear during the current review session.

Verba addresses this problem by maintaining a complete, searchable library of collected structures. Users should be able to access the entire library whenever they need it, without being restricted by a daily review schedule.

## 3. Core Design Principles

The following principles should guide all development decisions:

1. **Library first:** The complete collection of language patterns is the primary feature.

2. **Fast retrieval:** Users must be able to find a structure quickly while writing or practicing.

3. **Active language production:** The application should support the transition from recognizing a structure to using it independently.

4. **Simple data entry:** Adding, editing, and importing structures should require minimal effort.

5. **User-controlled learning:** Users decide what to study and when to study it. The application must not require every entry to be reviewed daily.

6. **Accuracy:** Grammar information and example sentences should be correct. AI-generated content must not be treated as automatically verified.

7. **Minimalism:** The initial version should focus on essential functionality rather than unnecessary features.

8. **Maintainability:** The application should have a clear architecture and allow future improvements without major rewrites.

## 4. Initial Technology Stack

The initial implementation will use the following technologies:

- Python

- Django

- Django REST Framework (DRF)

- SQLite

- HTML, CSS, and JavaScript for the web interface

Django will handle the backend, database models, authentication, business logic, and API endpoints.

Django REST Framework will provide the API used by the frontend.

SQLite will serve as the initial database and will be hosted on the application server.

The frontend should remain lightweight. A JavaScript framework is not required for the initial version.

The application will eventually be deployed to a server and made available through a custom domain managed with Cloudflare.

The architecture should avoid unnecessary dependencies and remain compatible with a future migration to PostgreSQL if operational requirements justify it.

## 5. Initial Architecture

The initial architecture is server-centric.

The browser communicates with the Django REST API. Django validates requests, applies authorization rules, and reads or modifies data in the server-side SQLite database.

The server is the authoritative source of application data.

A simplified architecture is:

Browser / Frontend → Django REST Framework API → Django Models / ORM → SQLite Database

The initial version does not require local database storage on user devices.

Cross-device access is achieved by retrieving data from the server after the user authenticates from another device.

Offline-first functionality and local database synchronization are explicitly outside the initial scope.

## 6. Core Data Model

The main entity is a language pattern.

A language pattern represents a reusable linguistic structure rather than necessarily a single vocabulary item.

Examples include:

- `warten auf + Akkusativ`

- `sich interessieren für + Akkusativ`

- `teilnehmen an + Dativ`

- `sich entscheiden für/gegen + Akkusativ`

A pattern may represent a verb-preposition combination, a collocation, a grammatical construction, or a useful expression.

Each pattern should support the following information.

### 6.1 Required Information

**Pattern**

The main language structure being learned.

Example: `sich interessieren für + Akkusativ`

**Example sentence**

A natural and grammatically correct sentence demonstrating the pattern.

Example: `Ich interessiere mich für Informatik.`

The example should be written in the target language.

### 6.2 Optional Information

**Translation**

A user-provided translation of the example sentence. Translation is optional because the learner may prefer to practice understanding the target language without relying on their native language.

**Notes**

An optional free-text field for explanations, grammatical details, usage restrictions, register, meaning distinctions, or other relevant information.

### 6.3 Additional Metadata

The internal data model may also include:

- Unique identifier

- Owner or user

- Pattern type

- Preposition and grammatical case, when applicable

- Tags or categories

- Creation timestamp

- Last modification timestamp

These fields should support future functionality without making the initial interface unnecessarily complicated.

The data model should distinguish between information essential to the pattern and optional metadata.

## 7. User Interface

The initial interface consists of three main pages.

### 7.1 Pattern List Page

This is the main page of Verba.

It displays all patterns available to the authenticated user in a numbered, readable list.

Each entry should provide a concise representation of the pattern. The interface should prioritize readability and quick navigation over decorative elements.

Essential features:

- Display the complete collection.

- Search patterns by text.

- Open a pattern's detail page by selecting an entry.

- Provide basic navigation and pagination when necessary.

- Preserve a clear and consistent layout.

The application must not hide patterns merely because they are not scheduled for review.

### 7.2 Pattern Detail Page

This page is primarily read-only.

It displays the information associated with a selected pattern:

1. The main pattern.

2. The example sentence in the target language.

3. The optional user-provided translation.

4. Optional notes and explanations.

An Edit action should allow the user to navigate to a separate editing page.

The detail page should prioritize readability and make the main pattern and its example easy to identify.

Users should not accidentally modify information while simply reading it.

### 7.3 Pattern Edit Page

This page contains a form for creating or editing a pattern.

Users should be able to modify:

- The main pattern.

- The example sentence.

- The optional translation.

- Optional notes.

The form should validate required fields, display useful error messages, and provide Save and Cancel actions.

Saving changes should persist them through the API. Canceling should return the user to the previous page without saving unintended changes.

The same form may be reused for creating new patterns, provided the implementation remains clear.

## 8. API and Backend Responsibilities

The backend is responsible for:

- Validating incoming data.

- Creating, retrieving, updating, and deleting patterns.

- Enforcing user ownership and authorization.

- Returning predictable API responses.

- Handling invalid requests and missing resources.

- Providing search and pagination when needed.

- Preventing unauthorized access to another user's private data.

The API should follow consistent REST conventions.

The initial implementation should focus on the operations required by the core interface rather than exposing unnecessary endpoints.

Authentication and authorization must be considered before the application is made publicly accessible.

## 9. AI-Assisted Data Entry

AI will be used as an optional assistant for extracting useful language patterns from existing learning activities.

Potential input sources include:

- Corrected writing exercises.

- Vocabulary sentence exercises.

- AI conversation transcripts.

- Notes collected while reading or listening.

The AI should identify reusable patterns and produce structured JSON.

A generated entry may contain the pattern, meaning, grammatical information, example sentences, optional translations, tags, and notes.

The JSON should be validated before it is imported into the application.

The import workflow should eventually support:

1. Receiving generated JSON.

2. Validating its structure and required fields.

3. Detecting possible duplicate patterns.

4. Previewing the proposed entries.

5. Allowing the user to approve or reject them.

6. Saving approved entries through the backend.

AI-generated grammar explanations and examples may contain errors. The application should allow users to inspect and correct entries rather than automatically assuming all generated content is accurate.

Full AI integration is not required for the first working version. Manual entry should work independently.

## 10. Initial Scope and Non-Goals

The first version should include only the functionality necessary to establish the core library.

### In Scope

- Server-side SQLite database.

- Django and Django REST Framework backend.

- Basic user authentication.

- User-owned language patterns.

- Pattern list page.

- Pattern detail page.

- Pattern creation and editing.

- Optional translations and notes.

- Basic search.

- Basic validation and error handling.

- Automated tests for important backend behavior.

- Initial server deployment.

### Out of Scope for the Initial Version

The following features should not delay the first usable release:

- A full spaced-repetition algorithm.

- Mandatory daily reviews.

- Advanced statistics and learning analytics.

- Complex AI integration.

- Automatic synchronization between local databases.

- Offline-first architecture.

- Native Android or iOS applications.

- Complex gamification.

- Microservices.

- Redis, Celery, or message queues without a demonstrated need.

These features may be considered later if real usage reveals a clear benefit.

## 11. Database and Deployment Considerations

SQLite is the initial database because the expected data consists primarily of text, examples, translations, and grammatical notes.

The initial application is expected to have relatively modest storage requirements.

However, database capacity should not be evaluated by disk space alone. Concurrent writes, request patterns, database locking, backup procedures, and hosting reliability must also be considered.

Django's ORM should be used for ordinary database operations. Database-specific dependencies should be minimized so that PostgreSQL remains a practical future option.

The deployed application must use secure configuration, protected secrets, HTTPS, appropriate Django production settings, and regular database backups.

Cloudflare will be used for domain and DNS management. It does not replace the need for a suitable host to run Django and store the database.

## 12. Future Development Possibilities

Future development should be guided by actual learning needs.

Possible additions include:

- JSON import and export.

- Improved duplicate detection.

- Tags and advanced filtering.

- A practice mode for constructing sentences.

- Tracking recurring mistakes.

- A list of patterns that need more practice.

- AI-assisted extraction and correction.

- Progressive Web App (PWA) support.

- Offline access through browser storage.

- Synchronization between local data and the server.

- Migration to PostgreSQL.

- Improved deployment and monitoring.

These possibilities are not commitments for the initial release. Each should be evaluated based on its usefulness and implementation cost.

## 13. Development Philosophy

Verba should be developed incrementally.

The first objective is to create a working application that reliably stores and displays language patterns.

Subsequent improvements should be added only after the underlying functionality is stable.

AI coding tools may be used to accelerate implementation, but generated code must be reviewed, tested, and understood.

Prefer clear models, small functions, straightforward API endpoints, and readable frontend code over premature abstraction.

The project should remain a practical learning tool rather than becoming an unnecessarily complex software engineering exercise.

## 14. Definition of a Successful Initial Release

The initial release is successful when a user can:

1. Access the application through a browser.

2. Authenticate securely.

3. Add a language pattern with an example.

4. Optionally add a translation and notes.

5. Browse the complete collection of their patterns.

6. Search for a pattern quickly.

7. Open a read-only detail page.

8. Edit an existing pattern through a separate page.

9. Access the same account and data from another device.

10. Rely on the server to preserve saved information, subject to normal service availability and backup protections.

At this stage, Verba does not need to replace Anki or implement sophisticated learning algorithms. Its core value is to provide a reliable, organized, and immediately accessible personal library of language patterns.

---

**Project Name:** Verba

**Primary Purpose:** A searchable personal library for collecting and reusing language patterns.

**Initial Target Language:** German

**Backend:** Django + Django REST Framework

**Database:** SQLite

**Frontend:** HTML + CSS + JavaScript

**Deployment:** Server-hosted web application with a custom domain managed through Cloudflare