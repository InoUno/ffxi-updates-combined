# Combined patch notes for all FFXI updates

[View the full notes here (Firefox recommended!)](https://inouno.github.io/ffxi-updates-combined/).

Chrome is not good for searching through all the pages, so Firefox is recommended here.

## Generation

The page is generated by taking all links to PlayOnline and the Square-Enix forum from [the BG updates list](https://www.bg-wiki.com/ffxi/Category:Update_History) and its subpages. This is done by `parse_bg_update_list.py`, which outputs the found links in a `.txt` file, which has then been pruned of any non-relevant links into the current `relevant_links.txt` file.

The script `download_pages.sh` utilizes the GNU utility `wget` to download all the given pages including styling and images.

Finally, the `generate_html.py` generates the final HTML page which iframes all the downloaded pages.