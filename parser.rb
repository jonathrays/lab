require 'net/http'
require 'uri'
require 'nokogiri'

$site = "http://www.mosigra.ru"
$Iterations = 10
$mailPattern = Regexp.new('[\w]+@[\w.]+[\w]')
start = [$site]
$urllist = [$site]
$index = 0
$mailslist = []
def req(urls)
  for url in urls do
    if $index < $Iterations - 1
      if url[0] == '/'
        url = $site+url
      end
      $index+=1
      uri = URI.parse(url)
      response = Net::HTTP.get_response(uri)
      content = response.body
      doc = Nokogiri::HTML(content)
      emails = content.scan($mailPattern).uniq
      $mailslist.push(emails)
      list  = doc.css("a")
      ur = Array.new
      list.each do |index|
        if index['href'].to_s.scan(/[@$#\s]/).size == 0 and index['href'].to_s.size > 1
          ur.push(index['href'].to_s)
        end
      end
      ur=ur-$urllist
      $urllist << ur
      req(ur)
    else
      break
    end
  end
end

req(start)
puts($mailslist.uniq)
