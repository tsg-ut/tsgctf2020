require 'json'

pubkey = JSON.parse(File.read('../dist/pubkey.json'))
e = pubkey['e']
d = pubkey['n']
cf = pubkey['cf']

c = File.read('../dist/output.txt').to_i

3.upto(e - 1) do |k|
  next unless (e * d - 1) % k == 0
  phi = (e * d - 1) / k

  c1 = (phi - 1) * cf + 1
  factors = [c1]
  2.upto(10) do |i|
    factors << i.pow(phi, c1) - 1
  end
  q = factors.reduce {|a, b| a.gcd(b)}
  next if q < 100

  p = phi / (q - 1) + 1
  n = p * q
  m = c.pow(d, n)

  puts([m.to_s(16)].pack('H*'))
end

