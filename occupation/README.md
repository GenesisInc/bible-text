# occupation

## usage - sample reports

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

- match

    ❯ task match -- shepherd | mlr --c2p --barred cat
        task: [match] uv run python3 bible.py --match "shepherd" --top-n 5 --csv
        +-----------+---------+-------+---------------------------------------------------------------------------------------+
        | book      | chapter | verse | text                                                                                  |
        +-----------+---------+-------+---------------------------------------------------------------------------------------+
        | john      | 10      | 14    | I am the fine shepherd. I know my sheep and my sheep know me,                         |
        | zechariah | 11      | 15    | And Jehovah said to me: Now take the equipment of a useless shepherd.                 |
        | john      | 10      | 2     | But the one who enters through the door is the shepherd of the sheep.                 |
        | zechariah | 11      | 4     | This is what Jehovah my God says, Shepherd the flock meant for the slaughter,         |
        | john      | 10      | 11    | I am the fine shepherd; the fine shepherd surrenders his life in behalf of the sheep. |
        +-----------+---------+-------+---------------------------------------------------------------------------------------+

- reference

    ❯ task ref -- genesis 1:1
        task: [ref] uv run python3 bible.py --reference "genesis 1:1"
        In the beginning God created the heavens and the earth.

    ❯ task ref -- genesis 1:1-1:6
        task: [ref] uv run python3 bible.py --reference "genesis 1:1-1:6"
        In the beginning God created the heavens and the earth. Now the earth was formless and desolate, and there was darkness upon the surface of the watery deep, and Gods active force was moving about over the surface of the waters. And God said: Let there be light. Then there was light. After that God saw that the light was good, and God began to divide the light from the darkness. God called the light Day, but the darkness he called Night. And there was evening and there was morning, a first day. Then God said: Let there be an expanse between the waters, and let there be a division between the waters and the waters.

    ❯ task ref -- genesis 1:25-2:2
        task: [ref] uv run python3 bible.py --reference "genesis 1:25-2:2"
        And God went on to make the wild animals of the earth according to their kinds and the domestic animals according to their kinds and all the creeping animals of the ground according to their kinds. And God saw that it was good. Then God said: Let us make man in our image, according to our likeness, and let them have in subjection the fish of the sea and the flying creatures of the heavens and the domestic animals and all the earth and every creeping animal that is moving on the earth. And God went on to create the man in his image, in Gods image he created him; male and female he created them. Further, God blessed them, and God said to them: Be fruitful and become many, fill the earth and subdue it, and have in subjection the fish of the sea and the flying creatures of the heavens and every living creature that is moving on the earth. Then God said: Here I have given to you every seed bearing plant that is on the entire earth and every tree with seed bearing fruit. Let them serve as food for you. And to every wild animal of the earth and to every flying creature of the heavens and to everything moving on the earth in which there is life, I have given all green vegetation for food. And it was so. After that God saw everything he had made, and look! it was very good. And there was evening and there was morning, a sixth day. Thus the heavens and the earth and everything in them were completed. And by the seventh day, God had completed the work that he had been doing, and he began to rest on the seventh day from all his work that he had been doing.
