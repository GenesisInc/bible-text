# occupation

## usage

- generate bible-data.json from files

        ❯ task generate-json
            task: [generate-json] uv run bible.py --generate

        Bible data successfully written to bible_data.json

Now, you have the whole bible in a single file: bible_data.json instead of ~1200 files.

- extract entities

        ❯ task extract
            task: [extract] uv run bible.py \
            --extract \
            --bible-json "bible_data.json" \
            --output-json "bible_entities.json" \
            --output-csv "bible_entities.csv"

        Entity and occupation extraction complete. JSON results saved to bible_entities.json
        CSV results saved to bible_entities.csv

Now, you have bible_entities.json bible_entities.csv with below summary of entities.

- summary of entities

        ❯ task summary
            +------------+-------+----------------------------------------------+
            | Type       | count | Explanation                                  |
            +------------+-------+----------------------------------------------+
            | PERSON     | 17662 | Names of individuals                         |
            | DATE       | 3432  | Explicit or implicit date expressions        |
            | GPE        | 9478  | Geopolitical entities (places)               |
            | ORG        | 4254  | Organizations or groups                      |
            | OCCUPATION | 5507  | Roles or professions                         |
            | NORP       | 1380  | Nationalities, religious or political groups |
            +------------+-------+----------------------------------------------+

- names recorded in the bible

        ❯ task names
            task: [names] mlr --c2p --barred --from bible_entities.csv \
            filter '$Type == "PERSON"' \
                then count-distinct -f Text \
                then label Names,Count \
                then head

            +---------+-------+
            | Names   | Count |
            +---------+-------+
            | God     | 15    |
            | Jehovah | 5161  |
            | bush    | 1     |
            | Havilah | 5     |
            | Gihon   | 2     |
            | Cush    | 10    |
            | Adam    | 20    |
            | Eve     | 3     |
            | Abel    | 18    |
            | Enoch   | 7     |
            +---------+-------+

- organizations mentioned

        ❯ task org
            task: [org] mlr --c2p --barred --from bible_entities.csv \
            filter '$Type == "ORG"' \
                then count-distinct -f Text \
                then label ORG_organization_or_groups,Count \
                then head

            +----------------------------+-------+
            | ORG_organization_or_groups | Count |
            +----------------------------+-------+
            | Pishon                     | 1     |
            | Cain                       | 13    |
            | Exile                      | 1     |
            | Afterward Cain             | 1     |
            | Lamech                     | 9     |
            | Tubal                      | 4     |
            | Adams                      | 2     |
            | Methuselah                 | 2     |
            | Nephilim                   | 3     |
            | Noahs                      | 4     |
            +----------------------------+-------+

- occupations

        ❯ task occupation
            task: [occupation] mlr --c2p --barred --from bible_entities.csv \
            filter '$Type == "OCCUPATION"' \
                then count-distinct -f Text \
                then label occupation,count

            +-------------+-------+
            | occupation  | count |
            +-------------+-------+
            | shepherd    | 129   |
            | slave       | 309   |
            | servant     | 828   |
            | king        | 2448  |
            | priest      | 957   |
            | prophet     | 459   |
            | elder       | 188   |
            | soldier     | 76    |
            | metalworker | 11    |
            | queen       | 29    |
            | scribe      | 65    |
            | fisherman   | 6     |
            | carpenter   | 2     |
            +-------------+-------+

- gpe (geo-political entities)

        ❯ task gpe
            task: [gpe] mlr --c2p --barred --from bible_entities.csv \
            filter '$Type == "GPE"' \
                then count-distinct -f Text \
                then label GPE_GeoPoliticalEntity,Count \
                then head

            +------------------------+-------+
            | GPE_GeoPoliticalEntity | Count |
            +------------------------+-------+
            | Eden                   | 16    |
            | Assyria                | 133   |
            | Jehovah                | 739   |
            | Adah                   | 6     |
            | Jubal                  | 1     |
            | Enosh                  | 1     |
            | Kenan                  | 6     |
            | Mahalalel              | 3     |
            | Methuselah             | 3     |
            | ark                    | 13    |
            +------------------------+-------+

- dates mentioned

        ❯ task date
            task: [date] mlr --c2p --barred --from bible_entities.csv \
            filter '$Type == "DATE" && $Book == "daniel"' \
                then head

            +--------+---------+-------+------+---------------------+
            | Book   | Chapter | Verse | Type | Text                |
            +--------+---------+-------+------+---------------------+
            | daniel | 1       | 1     | DATE | the third year      |
            | daniel | 1       | 5     | DATE | daily               |
            | daniel | 1       | 5     | DATE | three years         |
            | daniel | 1       | 7     | DATE | Shadrach            |
            | daniel | 1       | 12    | DATE | ten days            |
            | daniel | 1       | 14    | DATE | ten days            |
            | daniel | 1       | 15    | DATE | the end of ten days |
            | daniel | 1       | 21    | DATE | the first year      |
            | daniel | 2       | 1     | DATE | the second year     |
            | daniel | 2       | 28    | DATE | the days            |
            +--------+---------+-------+------+---------------------+

- date-summary

        ❯ task date-summary
            task: [date-summary] mlr --c2p --barred --from bible_entities.csv \
            filter '$Type == "DATE"' \
                then cut -f Text \
                then count-distinct -f Text \
                then head

            +-----------------+-------+
            | Text            | count |
            +-----------------+-------+
            | the light Day   | 1     |
            | a first day     | 1     |
            | a third day     | 1     |
            | between the day | 1     |
            | days            | 26    |
            | years           | 25    |
            | the day         | 312   |
            | day             | 9     |
            | a fourth day    | 1     |
            | a fifth day     | 1     |
            +-----------------+-------+
