#!/usr/local/bin/ruby -Ku
# -*- encoding: UTF-8 -*-
require 'time'
require 'cgi'

# クエリとパス情報の解析
params = CGI::parse(ENV['PATH_INFO'][/^.(.*)/, 1] || '').merge(CGI::parse(ENV['QUERY_STRING']))
def url_suffix(params)
  (ENV['QUERY_STRING'].empty? ? './' : './?') + params.map{|k, v| "#{k}=#{v}"}.join('&')
end

type = params['type'].first
cache_control = begin
                  q = params['cache-control'].first
                  q && q[/[\w,-=]*/]
                end
expires = case
          when ! cache_control                        then nil
          when ! cache_control.match(/max-age=(\d+)/) then nil
          else (Time.now + Regexp.last_match[1].to_i).httpdate
          end
last_modified = case params['last-modified'].first
                when 'now'  then Time.now.httpdate
                when '2000' then Time.local(2000, 1, 1).httpdate
                else nil
                end


# ランダムの色と形の情報を作成
Figure = Struct.new(:char, :r, :g, :b) do
  def self.random
    random_colors = [0, rand(256), 255].shuffle
    random_char = ['A'.unpack('c').first + rand(26)].pack('c')

    self.new(random_char, *random_colors)
  end
end

# ヘッダを生成
header = [
  "Status: 200 OK"
]
header << "Cache-Control: #{cache_control}" if cache_control
header << "Expires:       #{expires}"       if expires
header << "Last-Modified: #{last_modified}" if last_modified

# type を元にデータを送信: CSS / AJAX / html
case type
when 'style'
  header << "Content-Type: text/css"
  f = Figure.random
  print \
    header.join("\n") +
    "\n\n" +
    ".css-test { background-color: rgb(#{f.r}, #{f.g}, #{f.b}); display: none; }\n" +
    ".css-test.#{f.char}{ display: block; }"

when 'ajax'
  header << "Content-Type: text/html"
  f = Figure.random
  print \
    header.join("\n") +
    "\n\n" +
    "<p style='background-color: rgb(#{f.r}, #{f.g}, #{f.b})'>#{f.char}</p>"

else
  header << "Content-Type: text/html; charset=UTF-8"
  f = Figure.random
  print \
    header.join("\n") +
    "\n\n" +

    <<-EOS
    <html>
      <head>
        <style>
          .test { text-align: center; float:left; border: 1px solid gray; width: 10eM; }
          .test p { font: 200% bold; margin: 0; }
          h3 { font-size: 120% bold; margin: 0.2em; }
	  p.links { margin: 0; padding: 0; font-size: 80%; }
        </style>
        <link rel='stylesheet' type='text/css' href='#{url_suffix(params.merge('type' => 'style'))}'>
      </head>
      <body>

      <h3>Cache-Control: #{cache_control},<br>Last-Modified: #{last_modified}</h3>


      <div class='test'>
        <p style='background-color: rgb(#{f.r}, #{f.g}, #{f.b})'>#{f.char}</p>
        Inline HTML
      </div>

      <div class='test'>
        #{('A'..'Z').map{|c|"<p class='css-test #{c}'>#{c}</p>"}.join}
        CSS &lt;link&gt;
      </div>

      <div class='test'>
        <div id='ajax_result'></div>
        <script type='text/javascript'><!--
        var xhr = XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('MSXML2.XMLHTTP.6.0');
        xhr.onreadystatechange = function() {
          if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('ajax_result').innerHTML = xhr.responseText;
          }
        };
        xhr.open('GET', '#{url_suffix(params.merge('type' => 'ajax'))}');
        xhr.send();
        // --></script>
        XMLHttpRequest
      </div>

      <div style='clear: both'></div>


      <p class="links">
      条件:
      <a href='./?cache-control=private,max-age=0&last-modified=2000'>キャッシュ無し</a> 
      <a href='./?cache-control=private,max-age=60&last-modified=2000'>キャッシュ1分</a>
      <a href='./?last-modified=2000'>古い最終更新日</a>
      <a href='./?last-modified=now'>最近の最終更新日</a>
      <a href='./last-modified=2000'>古い最終更新日+クエリ文字列無し</a>
      <a href='./last-modified=now'>最近の最終更新日+クエリ文字列無し</a>
      <a href='./'>ヘッダ無し</a> 
      </p>
      </body>
    </html>
    EOS
end
