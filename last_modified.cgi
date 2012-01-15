#!/usr/local/bin/ruby -Ku
# -*- encoding: UTF-8 -*-
require 'time'

last_modified = Time.local(2011, 1, 9, 17, 30, 0)


# ヘッダからコンテンツが最新かどうかを判別
if_modified_since_header = ENV['HTTP_IF_MODIFIED_SINCE']
if if_modified_since_header && Time.httpdate(if_modified_since_header) == last_modified

  print \
    "Status: 304 Not Modified\n" +
    "Cache-Control: max-age=0, public, no-cache\n" +
    "\n"

else
  
  sleep(1)

  print \
    "Content-Type: text/plain; charset=UTF-8\n" +
    "Cache-Control: max-age=0, public, no-cache\n" +
    "Last-Modified: #{last_modified.httpdate}\n" +
    "\n" +
    "hello\n"
end
