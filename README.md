[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Amiou9/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Amiou9/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World on Wednesday, 25 November 2026

One image summing up the world's news of Wednesday, 25 November 2026 — built for the make.fun bounty "Sum up 25 November's world news in one image".

## The image

Version A (Klasik): a dense broadsheet front page on cream paper, with a serif masthead reading "Wednesday, 25 November 2026". Its three lead stories are the Shenzhou-24 launch carrying Pakistan's first astronaut, Muhammad Zeeshan Ali, to the Tiangong space station; the Trump tariff threat that sank tech stocks again (Nasdaq -2%, Nvidia -6%); and the hack of the CIA and ODNI unclassified intelligence network. Thirty-two further stories, each with its own original drawn illustration, and a realistic world map with every story numbered on it, fill the rest of the page, with a DATE CHECK footer naming the Tuesday 24 November stories left out (the FIFA Women's World Cup host announcement, Shubman Gill's call to lift the ICC saliva ban, and Babar Azam's ILT20 debut fifty).

## Contents

- 35 stories in all, each dated Wednesday 25 November 2026, with sources named beside each story
- 3 lead stories: Shenzhou-24 / Pakistan's first astronaut, the Trump tariff shock, the CIA breach
- 10 more illustrated stories: Putin's retaliation warning, Zelensky confirming the Sparta II strike, the Huawei verdict, Giuliani's Medal of Freedom, Iran's blockade vow, the Gaza strike, the Yemen strikes, the Nepal earthquake, the Champions League night, and the UNAIDS report
- 22 more stories in the "Also on Wednesday 25 November" list, from the Thanksgiving turkey pardons to the California king tides
- A world map with numbered dots at the correct countries, and a DATE CHECK footer

## The program

`main.py` (Python 3, standard library only, no network) validates `entry.png` in full — PNG signature, every chunk's checksum, IHDR length / bit depth / colour type / compression / filter / interlace, a non-empty IDAT that decompresses, a whole IEND chunk at the end, dimensions at most 1024×1024 and size at most 1 MiB — then writes an exact copy to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). Two runs write the same bytes.
