require 'rack/contrib'
require 'sinatra/base'
require 'sinatra/json'
require 'sqlite3'

class App < Sinatra::Base
  DB = SQLite3::Database.new 'data/db.sqlite3'
  DB.execute <<-SQL
    CREATE TABLE IF NOT EXISTS notes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id TEXT,
      content TEXT
    );
    
    CREATE TABLE IF NOT EXISTS tokens (
      id TEXT PRIMARY KEY,
      remain INTEGER
    );
  SQL

  DB.execute <<-SQL
    INSERT OR REPLACE INTO notes (id, user_id, content)
    VALUES (0, '#{ENV['FLAG_USER_ID']}', '#{ENV['FLAG_CONTENT']}');
  SQL

  use Rack::JSONBodyParser
  use Rack::Session::Cookie, secret: ENV['SECRET'], old_secret: ENV['OLD_SECRET']

  def err(code, message)
    [code, json({message: message})]
  end

  post '/api/register' do
    session[:user] = SecureRandom.hex(16)

    json({})
  end

  post '/api/logout' do
    session[:user] = nil

    json({})
  end

  get '/api/note' do
    return err(401, 'login first') unless user = session[:user]

    sleep 0.5

    begin
      res = DB.query 'SELECT id, content FROM notes WHERE user_id = ? ORDER BY id', user
      notes = []
      res.each do |row|
        notes << {id: row[0], content: row[1]}
      end
      res.close
    end

    json(notes)
  end

  post '/api/note' do
    return err(401, 'register first') unless user = session[:user]
    return err(403, 'no note :rolling_on_the_floor_laughing:') unless note = params[:note] and String === note and note.bytesize > 0
    return err(403, 'too large note') unless note.bytesize < 500

    begin
      res = DB.query 'SELECT COUNT(1) FROM notes WHERE user_id = ?', user
      row = res.next
      count = row && row[0]
      res.close
    end

    return err(403, 'too many notes') unless count < 50

    DB.execute 'INSERT INTO notes (user_id, content) VALUES (?, ?)', user, note

    json({})
  end

  delete '/api/note/:id' do
    return err(401, 'login first') unless user = session[:user]
    puts params[:id]
    return err(404, 'no note') unless id = params[:id] and (String === id or Integer === id) and id = id.to_i

    DB.execute 'DELETE FROM notes WHERE id = ? AND user_id = ?', id, user

    200
  end
end
