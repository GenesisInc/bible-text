# bible text - analysis & data science

A hobby project to load multiple translations of bibles into a JSON file.
Output JSON file will be used for bible analysis.

## requirements

- [go-task/task](https://github.com/go-task/task)
- [astral-sh/uv](https://github.com/astral-sh/uv)
- [miller](https://github.com/johnkerl/miller)
- [jqlang/jq](https://github.com/jqlang/jq) (optional)
- [py-nlp-spacy-uv](./README.nlp_helper.md)

## Load bible to JSON

If you have the bible text in files, we need to load them to a json file using below task.

- generate bible-data.json from files

        ❯ task jsonify-bibles
        task: [jsonify-gateway-bibles] uv run python3 main.py load-gateway \
        --input-dir data/bibles/bible_gateway \
        --output-dir data/tmp

        data successfully written to data/tmp/multi_translation.json
        task: [jsonify-jworg-bibles] uv run python3 main.py \
        load-jworg \
        --input-dir  data/bibles/jw_org/nwt \
        --output-dir data/tmp

        data successfully written to data/tmp/nwt_bible.json
        Merged nwt translation saved to data/tmp/multi_translation.json

Now, you have the whole nwt bible in a file & all translations in multi-translation.json

## NWT study edition
<!-- markdownlint-disable MD001 no-bare-urls -->

Gen - https://wol.jw.org/en/wol/d/r1/lp-e/1001070105
exo - https://wol.jw.org/en/wol/d/r1/lp-e/1001070106
lev - https://wol.jw.org/en/wol/d/r1/lp-e/1001070107
job - https://wol.jw.org/en/wol/d/r1/lp-e/1001070170

## asv

asv gen 6   - https://wol.jw.org/en/wol/b/r1/lp-e/bi22/1/6#s=2&study=discover
            - https://wol.jw.org/en/wol/b/r1/lp-e/bi22/1/7#study=discover
            - https://wol.jw.org/en/wol/b/r1/lp-e/bi22/66/7#study=discover

## rh - the emphasized bible

- https://wol.jw.org/en/wol/b/r1/lp-e/rh/1/1#study=discover
- https://wol.jw.org/en/wol/b/r1/lp-e/rh/1/2#study=discover
- https://wol.jw.org/en/wol/b/r1/lp-e/rh/66/1#study=discover
- https://wol.jw.org/en/wol/b/r1/lp-e/rh/19/150#study=discover
- https://www.jw.org/finder?wtlocale=E&pub=rh&srctype=wol&bible=19150000&srcid=share