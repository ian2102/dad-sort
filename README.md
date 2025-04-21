# dad-sort
dad-sort is an automated inventory sorting tool designed for the game Dark and Darker. It utilizes object detection via YOLOv5 and optical character recognition (OCR) via Tesseract to identify and categorize in-game items, streamlining stash management for players.

## Known Issues
- Tesseract OCR is sometimes unreliable, resulting in incorrect text parsing and failed item identification.
- There is a logic error or bug in the sorting algorithm, causing failed item placements.

## Contributing
Contributions are welcome!

## Acknowledgments
- Huge thanks to [DarkerDB](https://darkerdb.com/) and Anders on Discord for their support and for providing a custom Pytesseract model and YOLOv5 model.
- Shoutout to the [Dark and Darker Wiki](https://darkanddarker.wiki.spellsandguns.com/Dark_and_Darker_Wiki) and Sur on Discord for item data.
