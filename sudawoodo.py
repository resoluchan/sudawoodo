import os
import sys
import time
from asyncio import sleep, ensure_future

import discord
import pandas as pd
import jaconv


class Pokemon(discord.Client):
    def __init__(self):
        super(Pokemon, self).__init__()

        self.table = pd.read_csv(
            './pokemon.tsv', sep='\t', dtype=str
        ).fillna("")
        self.table['No.str'] = \
            self.table['No.'].apply(lambda x: f'No.{x}')

        self.table_moves = pd.read_csv(
            './pokemon_moves.tsv', sep='\t', dtype=str
        ).fillna("")
        self.table_moves_katakana_lower = \
            self.table_moves.applymap(
                lambda name: jaconv.hira2kata(name.lower())
            )

    async def on_message(self, message):
        if len(message.content) == 0:
            return

        content = message.content.lower()
        content_normalized = jaconv.hira2kata(content[0].upper() + content[1:])

        if content_normalized == 'No.???':
            return

        # filter pokemon list
        match = self.table[
            self.table.drop(columns='No.').applymap(
                lambda name: name == content_normalized
            ).any(axis=1)
        ]
        if len(match) != 0:
            # display 1st pokemon of filtered list (expected that only 1 item has been extracted)
            match = match.drop(columns='No.str')
            matchseq = match.iloc[0]
            embed = format_pokeinfo(zip(matchseq.index, matchseq))
            await message.channel.send(embed=embed)

        # filter move(waza) list
        content_normalized_lower = content_normalized.lower()
        match_moves = self.table_moves[
            self.table_moves_katakana_lower.applymap(
                lambda name: name == content_normalized_lower
            ).any(axis=1)
        ]
        if len(match_moves) != 0:
            # display 1st move of filtered list (expected that only 1 item has been extracted)
            matchseq_moves = match_moves.iloc[0]
            embed = format_pokeinfo(zip(matchseq_moves.index, matchseq_moves))
            await message.channel.send(embed=embed)


def format_pokeinfo(index_value_seq):
    name_jp = 'NO DATA'
    description = ''
    for index, value in index_value_seq:
        if index in ['日', '🇯🇵']:
            if value == '':
                continue
            name_jp = value
            continue
        description += (
            f'{index} [NO DATA]\n'
            if value == '' else
            f'{index} `{value}`\n'
        )
    title = name_jp
    description = description[:-1]
    return discord.Embed(title=title, description=description)


if __name__ == '__main__':
    print("sudawoodo has started")
    poke = Pokemon()
    poke.run(os.getenv('DISCORD_BOT_TOKEN'))
