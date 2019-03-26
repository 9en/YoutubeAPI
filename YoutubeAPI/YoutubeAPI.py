#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import requests
import json
import pandas as pd
import sys
import os

class YoutubeAPI:
    '''
    Description::
        YoutubeAPIを利用してデータを取得する
    :param youtube_url:
        youtubeを再生するURL
    :param config_filename
        設定ファイル名を指定する
    Usage::
    >>> import YoutubeAPI
    '''
    def __init__(self, youtube_url, config_filename):
        self.VIDEOID = youtube_url.split('=')[1]
        cfgparser = configparser.ConfigParser()
        cfgparser.optionxform = str
        cfgparser.read(config_filename, 'UTF-8')
        self.API_URL = cfgparser.get('settings', 'URL')
        self.PARAM = {}
        self.PARAM['commentThreads'] = dict(cfgparser.items('commentThreads'))
        self.PARAM['commentThreads']['maxResults'] = int(self.PARAM['commentThreads']['maxResults'])
        self.PARAM['videos'] = dict(cfgparser.items('videos'))
        self.PARAM['videos']['id'] = self.VIDEOID
        self.PARAM['commentThreads']['videoId'] = self.VIDEOID

    def get_api_requests(self, kind, token={}):
        return requests.get(self.API_URL + kind, params={**self.PARAM[kind], **token}).json()

    def extract_data(self, response, extract_list, kind):
        for items in response['items']:
            if kind == 'commentThreads':
                extract_list.append([
                    items['snippet']['topLevelComment']['snippet']['publishedAt'][:10],
                    items['snippet']['topLevelComment']['snippet']['publishedAt'],
                    items['id'],
                    items['snippet']['videoId'],
                    items['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    items['snippet']['topLevelComment']['snippet']['authorChannelId']['value'],
                    items['snippet']['topLevelComment']['snippet'].get('likeCount',0),
                    items['snippet'].get('totalReplyCount',0),
                    items['snippet']['topLevelComment']['snippet']['textDisplay'].replace('\n',' ').replace('\t',' '),
                ])
            elif kind == 'videos':
                extract_list.append([
                    items['snippet']['publishedAt'][:10],
                    items['snippet']['publishedAt'],
                    items['snippet']['channelId'],
                    items['snippet']['channelTitle'].replace('\t', ' '),
                    self.VIDEOID,
                    items['snippet']['title'].replace('\t', ' '),
                    items['snippet']['thumbnails']['maxres']['url'],
                    ','.join(items['snippet']['tags']).replace('\t', ' '),
                    items['statistics'].get('viewCount',0),
                    items['statistics'].get('likeCount',0),
                    items['statistics'].get('dislikeCount',0),
                    items['statistics'].get('favoriteCount',0),
                    items['statistics'].get('commentCount',0)
                ])
        return extract_list

    def get_comment_data(self, get_dt=False):
        '''
        Description::
            コメント一覧を取得する（コメントの返信は含まない）
        Retern::
            動画を公開した日付（YYYY-MM-DD）
        Output::
            output_comment.tsv
            カラム：dt,publishedAt,id,videoId,authorDisplayName,authorChannelId,likeCount,totalReplyCount,textDisplay
            ※[reference](https://developers.google.com/youtube/v3/docs/comments)
        Param::
            get_dt:
                True / False(デフォルト)
                動画公開日(YYYY-MM-DD)を取得する

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
        '''
        extract_list = []
        kind = 'commentThreads'
        response = self.get_api_requests(kind)
        counter = 0
        while response.get('nextPageToken'):
            try:
                print('extract ' + str(counter) + ' page (100comment/1page)')
                extract_list = self.extract_data(response, extract_list, kind)
                response = self.get_api_requests(kind, {'pageToken':response.get('nextPageToken')})
                counter += 1
            except Exception:
                break
        pd.DataFrame(extract_list).to_csv(os.getcwd() + '/output_comment.tsv', sep='\t', index=False, header=False)
        if get_dt:
            response = self.get_api_requests('videos')
            return response['items'][0]['snippet']['publishedAt'][:10]

    def get_video_data(self, get_dt=False):
        '''
        Description::
            動画の基礎数値
        Retern::
            動画を公開した日付（YYYY-MM-DD）
        Output::
            output_video.tsv
            カラム：dt,publishedAt,channelId,channelTitle,videoId,title,thumbnails,tags,viewCount,likeCount,dislikeCount,favoriteCount,commentCount
            ※[reference](https://developers.google.com/youtube/v3/docs/videos)
        Param::
            get_dt:
                True / False(デフォルト)
                動画公開日(YYYY-MM-DD)を取得する

        Sample::
        >>> import YoutubeAPI
        >>> youtube_url = 'https://www.youtube.com/watch?v=SjQaPt68o0M'
        >>> config_filename = 'config.ini'
        >>> yt = YoutubeAPI.YoutubeAPI(youtube_url, config_filename)
        >>> yt.get_video_data()
        '''
        extract_list = []
        kind = 'videos'
        response = self.get_api_requests(kind)
        try:
            extract_list = self.extract_data(response, extract_list, kind)
            response = self.get_api_requests(kind)
        except Exception:
            pass
        pd.DataFrame(extract_list).to_csv(os.getcwd() +'/output_video.tsv', sep='\t', index=False, header=False)
        if get_dt:
            return extract_list[0][0]

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)