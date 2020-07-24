require 'base64'

patterns = []

[0].product(
  [4, 5, 6, 7],
  [4, 5, 6, 7],
  [2, 6],
) do |pattern|
  patterns << pattern.join.to_i
end

[0].product(
  [0, 1, 2, 3],
  [4, 5, 6, 7],
  [0, 1, 4, 5, 8, 9],
) do |pattern|
  patterns << pattern.join.to_i
end

ra, rb, numerator, denominator = 0, 0, 0, 0
loop do
  numerator = patterns.sample
  denominator = patterns.select {|v| v >= 100}.sample * 10 + rand(10)
  target = Math::PI - numerator.fdiv(denominator)
  next if target < 0.5

  ra, rb = 0, 0
  4.times do |k|
    mindiff = 10000
    minpat = nil
    patterns.each do |a|
      patterns.each do |b|
        next if k == 0 && b < 100
        max = (ra * 10000 + a * 10 + 9).fdiv(rb * 10000 + b * 10)
        min = (ra * 10000 + a * 10).fdiv(rb * 10000 + b * 10 + 9)
        if min <= target && target <= max
          10.times do |i|
            10.times do |j|
              ret = (ra * 10000 + a * 10 + i).fdiv(rb * 10000 + b * 10 + j)
              if (target - ret).abs < mindiff
                mindiff = (target - ret).abs
                minval = ret
                minpat = [a, i, b, j]
              end
            end
          end
        end
      end
    end
    a, i, b, j = minpat
    ra = ra * 10000 + a * 10 + i
    rb = rb * 10000 + b * 10 + j
    p [ra, rb]
  end

  result = (ra / 10).fdiv(rb / 10) + numerator.fdiv(denominator)
  if result == Math::PI
    p ra, rb, numerator, denominator
    break
  end
end

exploit_txt = "#{ra.to_s[...-1]}/#{rb.to_s[...-1]}+#{numerator}/#{denominator}"
exploit = Base64.decode64(exploit_txt)
File.write('solution.txt', exploit)

puts exploit_txt
puts exploit
