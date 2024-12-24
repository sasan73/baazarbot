from datetime import datetime as dt
from pathlib import Path

import click

from baazarbot import settings
from pipelines import digital_data_etl

@click.command()
@click.option("--no-cache", is_flag=True, default=False, help="Option to disable cache.")
@click.option("--run-etl", is_flag=True, default=False, help="Option to run digital data ETL.")
@click.option("--export_settings", is_flag=True, default=False, help="Option to export settings to ZenML secrets.")
@click.option("--etl-config-filename", default="digital_data_etl.yml", help="ETL configuration filename.")
def main(
    no_cache: bool,
    run_etl: bool,
    export_settings: bool,
    etl_config_filename: str = "digital_data_etl.yml",
) -> None:
    """Main method to run the script."""
    assert(
        no_cache or
        run_etl
    ), "Please specify at least one option."

    pipeline_args = {
        "enable_cache": not no_cache,
    }

    # if export_settings:
    #     logger.info("Exporting settings to ZenML secrets.")
    #     settings.export()
    
    root_dir = Path(__file__).resolve().parent.parent
    
    if run_etl:
        run_args_etl = {}
        pipeline_args["config_path"] = root_dir / "configs" / etl_config_filename
        assert pipeline_args["config_path"].exists(), f"Config file not found: {pipeline_args['config_path']}"
        pipeline_args["run_name"] = f"digital_data_etl_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        digital_data_etl.with_options(**pipeline_args)(**run_args_etl)

if __name__ == "__main__":
    main()
