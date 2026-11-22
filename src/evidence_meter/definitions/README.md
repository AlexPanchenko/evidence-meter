# Definitions

The versioned catalogue of metric definitions: formula id, inputs, minimum data, version. It loads the
private definitions file at run time and never writes it; nothing else reads that file.

- **Terms:** MetricDefinition, DefinitionVersion, Formula, MinimumData.
- **Publishes:** `DefinitionVersionPublished`.
- **Listens to:** nothing.
- **Structure:** handler/service/repo.
