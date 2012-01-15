#!/usr/local/bin/ruby -Ku
# -*- encoding: UTF-8 -*-
require 'time'

patent_name = '雪見だいふく'
patent_id = 1537351

# ヘッダからコンテンツが最新かどうかを判別
if_none_match_header = ENV['HTTP_IF_NONE_MATCH']
if if_none_match_header && if_none_match_header == "\"#{patent_id}\""

  print \
    "Status: 304 Not Modified\n" +
    "Cache-Control: max-age=0, public, no-cache\n" +
    "\n"

else

  sleep(1)

  print \
    "Content-Type: text/plain; charset=UTF-8\n" +
    "Cache-Control: max-age=0, public, no-cache\n" +
    "ETag: \"#{patent_id}\"\n" +
    "\n" +
    "#{patent_name} の特許の番号は #{patent_id} だった。\n" +
    "前から読んでも後ろから読んでも同じ!\n"
end
