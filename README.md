# Overview
YoutubeのAPIを使ってデータを取得するパッケージ

# Requirements

* Python (>= 3.4)

# Setting up
```
pip install git+https://github.com/9en/YoutubeAPI
```

# Usage
## get_comment_data
* Description:
    * コメント一覧を取得する（コメントの返信は含まない）
* Retern:
    * 動画を公開した日付（YYYY-MM-DD）
* Param::
    * get_dt:
        * True / False(デフォルト)
        * 動画公開日(YYYY-MM-DD)を取得する
* Output:
    * ファイル名：output_comment.tsv
    * カレントディレクトに出力する
    * カラム([reference](https://developers.google.com/youtube/v3/docs/comments))：
        * dt
        * publishedAt
        * id,videoId
        * authorDisplayName
        * authorChannelId
        * likeCount
        * totalReplyCount
        * textDisplay

```
Sample::
>>> import YoutubeAPI
>>> youtube_url = 'https://www.youtube.com/watch?v=SjQaPt68o0M'
>>> config_filename = 'config.ini'
>>> yt = YoutubeAPI.YoutubeAPI(youtube_url, config_filename)
>>> yt.get_comment_data()
extract 0 page (100comment/1page)
extract 1 page (100comment/1page)
extract 2 page (100comment/1page)
extract 3 page (100comment/1page)
extract 4 page (100comment/1page)
extract 5 page (100comment/1page)
extract 6 page (100comment/1page)
extract 7 page (100comment/1page)
extract 8 page (100comment/1page)
extract 9 page (100comment/1page)
```


## get_comment_data
* Description:
    * 動画の基礎数値
* Retern:
    * 動画を公開した日付（YYYY-MM-DD）
* Param::
    * get_dt:
        * True / False(デフォルト)
        * 動画公開日(YYYY-MM-DD)を取得する
* Output:
    * ファイル名：output_video.tsv
    * カレントディレクトに出力する
    * カラム([reference](https://developers.google.com/youtube/v3/docs/videos))：
        * dt
        * publishedAt
        * channelId
        * channelTitle
        * videoId
        * title
        * thumbnails
        * tags
        * viewCount
        * likeCount
        * dislikeCount
        * favoriteCount
        * commentCount

```
Sample::
>>> import YoutubeAPI
>>> youtube_url = 'https://www.youtube.com/watch?v=SjQaPt68o0M'
>>> config_filename = 'config.ini'
>>> yt = YoutubeAPI.YoutubeAPI(youtube_url, config_filename)
>>> yt.get_video_data()
```

# make config.ini
`<APIトークン>` は[こちらのサイト](https://developers.google.com/youtube/registering_an_application?hl=ja)を参考にから取得する
```
[settings]
URL: https://www.googleapis.com/youtube/v3/

[commentThreads]
key: <APIトークン>
part: snippet
order: relevance
textFormat: plaintext
maxResults: 100

[videos]
key: <APIトークン>
part: snippet,statistics
```


