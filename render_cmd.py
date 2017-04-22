from article_summarizer import summarize_article
import json
import os
import random
import subprocess

import datetime
import time
from clients.feedly.feedly_client import FeedlyClient
from download_utils import download_url_to_file
import video_tweet
from ffmpeg_utils import encode_to_mp4
from google_shorten_url import shorten_url

now = datetime.datetime.now()
then = now - datetime.timedelta(hours=3)
timestamp = time.mktime(then.timetuple()) * 1e3
feedly_client = FeedlyClient()
# feed_list = ['feed/http://www.engadget.com/rss-full.xml',
#              'feed/http://feeds.gawker.com/lifehacker/vip',
#              'feed/http://feeds.wired.com/wired/index',
#              'feed/http://www.theverge.com/rss/full.xml',
#              'feed/http://feeds.feedburner.com/Techcrunch',
#              'feed/http://www.polygon.com/rss/index.xml',
#              'feed/http://feeds.gawker.com/kotaku/vip',
#              'feed/http://feeds.ign.com/ign/games-all',
#              'feed/http://www.lemonde.fr/rss/sequence/0,2-3208,1-0,0.xml',
#              'feed/http://www.lefigaro.fr/rss/figaro_une.xml',
#              'feed/http://rss.liberation.fr/rss/latest/',
#              'feed/http://www.20minutes.fr/rss/france.xml',
#              'feed/http://www.lequipe.fr/Xml/Football/Titres/actu_rss.xml',
#              'feed/http://www.footmercato.net/spip.php?page=backend&id_rubrique=23'
#              ]

# feed_list = ['feed/http://feeds2.feedburner.com/thenextweb',
#              'feed/http://www.readwriteweb.com/rss.xml',
#              'feed/http://www.macrumors.com/macrumors.xml',
#              'feed/http://www.androidcentral.com/feed',
#              'feed/http://feeds.arstechnica.com/arstechnica/index/',
#              'feed/http://feeds.mashable.com/Mashable',
#              'feed/http://feeds.gawker.com/gizmodo/full',
#              'feed/http://www.engadget.com/rss-full.xml',
#              'feed/http://feeds.gawker.com/lifehacker/vip',
#              'feed/http://feeds.wired.com/wired/index',
#              'feed/http://www.theverge.com/rss/full.xml',
#              'feed/http://feeds.feedburner.com/Techcrunch',
#
#              'feed/http://www.polygon.com/rss/index.xml',
#              'feed/http://feeds.gawker.com/kotaku/vip',
#              'feed/http://feeds.ign.com/ign/games-all'
#               ]
feed_list = [
             'feed/http://www.tmz.com/category/gossip-rumors/rss.xml',
             'feed/http://feeds.feedburner.com/fashionistacom',
             'feed/http://www.fashionologie.com/posts/feed'
             'feed/http://feeds.feedburner.com/fitsugar',
             'feed/http://feeds.feedburner.com/bellasugar',
             'feed/http://feeds.feedburner.com/buzzsugar',
             'feed/http://feeds.feedburner.com/yumsugar',
             'feed/http://feeds.feedburner.com/casasugar',
#
#
#              'feed/http://www.engadget.com/rss-full.xml',
#              'feed/http://feeds.gawker.com/lifehacker/vip',
#              'feed/http://feeds.wired.com/wired/index',
#              'feed/http://www.theverge.com/rss/full.xml',
#              'feed/http://feeds.feedburner.com/Techcrunch',
#
#              'feed/http://www.polygon.com/rss/index.xml',
#              'feed/http://feeds.gawker.com/kotaku/vip',
#              'feed/http://feeds.ign.com/ign/games-all',
#
             'feed/http://sports.espn.go.com/espn/rss/news',
             'feed/http://rss.cnn.com/rss/si_topstories.rss',
             'feed/http://rss.news.yahoo.com/rss/sports',
             'feed/http://www.nfl.com/rss/rsslanding?searchString=home',
             'feed/http://sports.espn.go.com/espn/rss/nfl/news',
             'feed/http://msn.foxsports.com/feedout/syndicatedContent?categoryId=5',
             'feed/http://sports.yahoo.com/nfl/rss.xml',
             'feed/http://www.nba.com/rss/nba_rss.xml',
             'feed/http://sports.espn.go.com/espn/rss/nba/news',
             'feed/http://sports.yahoo.com/nba/rss.xml',
             'feed/http://www.theguardian.com/football/rss',
             'feed/http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/football/rss.xml',
             'feed/http://www.skysports.com/rss/0,20514,11095,00.xml',
             'feed/http://www.101greatgoals.com/feed/'

             ]

output_files = []

for feed in feed_list:
    results = json.loads(json.dumps(feedly_client.getMix(feed, '2', '4', '0', 'en')))
    items = results["items"]
    for item in items:
        if item.get('visual'):
            if item['visual'].get('url') and item['visual']['url'] != 'none':
                try:
                    # # RENDER VISUAL
                    # imageFilePath = os.getcwd() + '/temp/' + os.path.basename(item['visual']['url'])
                    # download_url_to_file(item['visual']['url'], imageFilePath)
                    # visual_intro_file_path = os.path.splitext(os.path.basename(imageFilePath))[0] + '.mp4'
                    #
                    # cmd_render_text_layer = 'blender -b ' + os.getcwd() + '/blender_files/V_array_visual.blend -P render_v_array_intro.py -- --image ' \
                    #                         + '"' + imageFilePath \
                    #                         + '" --output ' \
                    #                         + '"' + os.getcwd() + '/temp/' + \
                    #                         os.path.splitext(os.path.basename(imageFilePath))[0] + '.mp4' + '"'
                    # print(cmd_render_text_layer)
                    # subprocess.call(cmd_render_text_layer, shell=True, stderr=subprocess.PIPE)
                    #
                    # # RENDER TEXT LAYER
                    # intro_text_layer_file_path = os.getcwd() + '/temp/' + item['title'] + '.mp4'
                    # cmd_render_text_layer = 'blender -b ' + os.getcwd() + '/blender_files/V_title_center.blend -P render_v_text_center_intro.py -- --title ' \
                    #                         + '"' + item["title"] \
                    #                         + '" --output ' \
                    #                         + '"' + intro_text_layer_file_path + '"'
                    # print(cmd_render_text_layer)
                    # subprocess.call(cmd_render_text_layer, shell=True, stderr=subprocess.PIPE)
                    #
                    # # BLEND VISUAL + TEXT LAYER
                    # output_file_path = os.getcwd() + '/temp/' + os.path.splitext(os.path.basename(imageFilePath))[
                    #     0] + '_intro' + '.mp4'
                    # cmd_render_text_layer = 'blender -b -P render_blend_intro.py -- --visual_file_path ' \
                    #                         + '"' + os.getcwd() + '/temp/' + visual_intro_file_path \
                    #                         + '" --title_file_path ' \
                    #                         + '"' + intro_text_layer_file_path \
                    #                         + '" --output ' \
                    #                         + '"' + output_file_path + '"'
                    #
                    # print(cmd_render_text_layer)
                    # subprocess.call(cmd_render_text_layer, shell=True, stderr=subprocess.PIPE)
                    # output_files.append(output_file_path)

                    # INTRO

                    # Download visual
                    imageFilePath = os.getcwd() + '/temp/' + os.path.basename(item['visual']['url'])
                    download_url_to_file(item['visual']['url'], imageFilePath)

                    intro_file_path = os.getcwd() + '/temp/' + item["title"] + '_intro.mp4'
                    intro_blender_file_path = os.getcwd() + '/blender_files/S_array_intro_2.blend'
                    cmd_render_intro = 'blender -b ' + intro_blender_file_path + ' -P render_intro.py -- --image ' \
                                       + '"' + imageFilePath \
                                       + '" --title ' \
                                       + '"' + item["title"] \
                                       + '" --output ' \
                                       + '"' + intro_file_path + '"'
                    print(cmd_render_intro)
                    if not os.path.exists(intro_file_path):
                        print(intro_file_path + ' DOES NOT exist')
                        subprocess.call(cmd_render_intro, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    else:
                        print (imageFilePath + ' already exists')
                    output_files.append(intro_file_path)

                    # SUMMARY
                    summary = summarize_article(item["title"], item['alternate'][0]['href'])
                    summary_file_path = os.getcwd() + '/temp/' + item["title"] + '_summary.mp4'

                    summary_blender_file_path = os.getcwd() + '/blender_files/summary.blend'
                    cmd_render_summary = 'blender -b ' + summary_blender_file_path + ' -P render_summary.py -- --list_summary ' \
                                         + '"' + '" "'.join(summary) \
                                         + '" --output ' \
                                         + '"' + summary_file_path + '"'
                    print(cmd_render_summary)
                    if not os.path.exists(summary_file_path):
                        print(summary_file_path + ' DOES NOT exist')
                    else:
                        print(summary_file_path + ' already exist')
                        subprocess.call(cmd_render_summary, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output_files.append(summary_file_path)

                    final_output_file_path = os.getcwd() + '/temp/' + item["title"] + '.mp4'
                    # music_file_path = '/home/belgaloo/PycharmProjects/SoVibes/resources/In My Ears.mp3'
                    music_file_path = '/home/belgaloo/PycharmProjects/SoVibes/resources/Tropic.mp3'
                    outro_file_path = '/home/belgaloo/PycharmProjects/SoVibes/resources/outro_square_thumbs_up.mp4'
                    cmd_render_final = 'blender -b -P render_blend.py -- --list_movie_files ' \
                                       + '"' + '" "'.join(output_files) \
                                       + '" --outro_file_path ' \
                                       + '"' + outro_file_path \
                                       + '" --music_file_path ' \
                                       + '"' + music_file_path \
                                       + '" --resolution "1080x1080' \
                                       + '" --output ' \
                                       + '"' + final_output_file_path + '"'
                    print(cmd_render_final)
                    if not os.path.exists(final_output_file_path):
                        print(final_output_file_path + ' DOES NOT exist')
                        subprocess.call(cmd_render_final, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                        final_encoded_file_path = encode_to_mp4(final_output_file_path)

                        # os.remove(os.getcwd() + '/temp/' + visual_intro_file_path)
                        # os.remove(intro_text_layer_file_path)
                        status = item["title"]
                        status = '#' + ' #'.join(status.split())
                        status += ' ' + shorten_url(item['alternate'][0]['href'])
                        tweet_video = video_tweet.VideoTweet(final_encoded_file_path)
                        tweet_video.upload_init()
                        tweet_video.upload_append()
                        tweet_video.upload_finalize()
                        tweet_video.tweet(status)
                    else:
                        print(final_output_file_path + ' already exist')

                    output_files.clear()
                except:
                    output_files.clear()
                    print('Erreur de rendu')

# STITCH INTROS
final_output_file_path = os.getcwd() + '/temp/tech_' + str(random.randint(0, 10000)) + '.mp4'
# music_file_path = '/home/belgaloo/PycharmProjects/SoVibes/resources/In My Ears.mp3'
music_file_path = '/home/belgaloo/PycharmProjects/SoVibes/resources/Tropic.mp3'
cmd_render_text_layer = 'blender -b -P render_blend.py -- --list_movie_files ' \
                        + '"' + '" "'.join(output_files) \
                        + '" --music_file_path ' \
                        + '"' + music_file_path \
                        + '" --output ' \
                        + '"' + final_output_file_path + '"'
print(cmd_render_text_layer)
# subprocess.call(cmd_render_text_layer, shell=True, stderr=subprocess.PIPE)


# cmd_render_text_layer = 'blender -b ' + os.getcwd() + '/kenburns_effect.blend -P render_kenburnseffect_random.py -- --image ' \
#           + '"' + imageFilePath \
#           + '" --output ' \
#           + '"' + os.getcwd() + '/temp/' + os.path.splitext(os.path.basename(imageFilePath))[0] + '.mp4'+ '"'



# for item in items:
#     if item.get('visual'):
#         if item['visual'].get('url'):
#             imageFilePath = os.getcwd() + '/temp/' + os.path.basename(item['visual']['url'])
#             download_url_to_file(item['visual']['url'], imageFilePath)
#
#             cmd_render_text_layer = 'blender -b ' + os.getcwd() + '/orthographic_square_default.blend -P render_kenburnseffect.py -- --image ' \
#                       + '"' + imageFilePath \
#                       + '" --output ' \
#                       + '"' + os.getcwd() + '/temp/' + os.path.splitext(os.path.basename(imageFilePath))[0] + '.mp4'+ '"'
#
#             print(cmd_render_text_layer)
#             subprocess.call(cmd_render_text_layer, shell=True, stderr=subprocess.PIPE)
