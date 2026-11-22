# Definitions

The versioned catalogue of metric definitions: formula id, inputs, minimum data, version. It loads the
private definitions file at run time and never writes it; nothing else reads that file.

- **Terms:** MetricDefinition, DefinitionVersion, Formula, MinimumData.
- **Publishes:** `DefinitionVersionPublished`, `DefinitionVersionRetired` (a version may no longer be used
  for new values; values already computed with it keep it).
- **Listens to:** nothing.
- **Structure:** handler/service/repo.
