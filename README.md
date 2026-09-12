### AI-Router Analysis

This project was developed to collect datapoints from [OpenRouter](https://openrouter.com) and [Hugging Face](https://hugginface.co) as a part of the group project for module M162E.

## Usage
Before using this project, you need to install [UV](https://docs.astral.sh/uv/]. Follow the official [installation guide](https://docs.astral.sh/uv/getting-started/installation/) to get started. 

Once (UV)[https://docs.astral.sh/uv/] is installed, you can fetch the data by running:
```bash
uv run fetch > <output-file>.csv
```

The resulting data is not sorted by default. To sort it from the highest price to the lowest price run:

```bash
uv run sort -f <output-file>.csv > <output-file-sorted.csv> 
```

## License
This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). For more information, see the [LICENSE.md](LICENSE.md) file. 

