require 'openssl'
require 'json'

def modinv(a, m)
  m0, inv, x0 = m, 1, 0
  while a > 1
    inv -= (a / m) * x0
    a, m = m, a % m
    inv, x0 = x0, inv
  end
  inv += m0 if inv < 0
  inv
end

class RSA
  def initialize
    @p = OpenSSL::BN::generate_prime(1024, true).to_i
    @q = OpenSSL::BN::generate_prime(1024, true).to_i
    @n = @p * @q
    @e = 65537
    @d = modinv(@e, (@p - 1) * (@q - 1))
    @exp1 = @d % (@p - 1)
    @exp2 = @d % (@q - 1)
    @cf = modinv(@q, @p)
  end

  def encrypt(m)
    m.pow(@e, @n)
  end

  def decrypt(c)
    m1 = c.pow(@exp1, @p)
    m2 = c.pow(@exp2, @q)
    (m2 + @cf * (m1 - m2) % @p * @q) % @n
  end

  def pubkey
    privkey.to_a[..2].to_h
  end

  def privkey
    {
      e: @e,
      n: @d,
      cf: @cf,
      p: @p,
      q: @q,
      exp1: @exp1,
      exp2: @exp2,
    }
  end
end

flag = File.read('flag.txt').unpack("H*")[0].hex
rsa = RSA.new
p rsa.encrypt(flag)

File.write('pubkey.json', JSON.dump(rsa.pubkey))
