from wepps.stage.stages import DocsStage, SettingsStage, PlotsStage

from typing import Any


class ResponseError(Exception):
    pass


class ResponseStages:

    def __init__(self) -> None:
        self.docs: list[DocsStage] = []
        self.settings: list[SettingsStage] = []
        self.plots: list[PlotsStage] = []

    def add_docs_stage(self, docs_stage: DocsStage) -> None:
        self.docs.append(docs_stage)

    def add_settings_stage(self, settings_stage: SettingsStage) -> None:
        self.settings.append(settings_stage)

    def add_plot_stage(self, plots_stage: PlotsStage) -> None:
        self.plots.append(plots_stage)

    def get_stages(
            self
    ) -> tuple[list[DocsStage], list[SettingsStage], list[PlotsStage]]:
        return (self.docs, self.settings, self.plots)


class App:

    def __init__(self, title) -> None:
        self.title = title
        if self.title == '':
            raise NotImplementedError('App has no title')
        self.docs: list[DocsStage] = []
        self.settings: list[SettingsStage] = []
        self.plots: list[PlotsStage] = []

    def compute(self, response_data: dict[str, Any] | None) -> ResponseStages:
        # response is None on initial request
        raise NotImplementedError('compute in App not implemented')
