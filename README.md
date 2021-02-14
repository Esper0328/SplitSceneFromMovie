# splitSceneFromMovie
The purpose of this script is effective edit of movie files (especially for my underwater movies).

## Environment
* Python 3.8.1
* macOS Catalina 10.15.7
* ffmpeg

## Usage
python splitSceneFromMovie.py MovieFilename.mp4, then you can get split movie file based on scene change under ./movie folder.
Currently only mp4 file is applicable.
You can regorganize a movie file by executing "ffmpeg -f concat -i sceneList.txt -c copy output.mp4" after editing sceneList.txt.
ffmpeg is available by executing　"brew install ffmpeg”

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## link
This program was made by seeing following link and improving
https://qiita.com/otakoma/items/842b7417b1012fab9097
