# Reporting

Turns accepted values and refusals into a monthly page per team and keeps the draft, the review and the
publication. Team-level only: no value per person.

- **Terms:** MonthlyPage, PageState, Review, Publication.
- **Publishes:** `PageDrafted`, `PageReviewed`, `PagePublished`.
- **Listens to:** `ValueAccepted`, `ValueRefused`, `CollectionFailed`.
- **Structure:** handler/service/repo.
