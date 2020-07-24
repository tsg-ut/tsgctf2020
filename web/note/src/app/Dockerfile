FROM ruby:2.6.3-alpine

RUN apk add --no-cache build-base sqlite-dev sqlite-libs 

COPY Gemfile /app/Gemfile

RUN cd /app && \
        bundle install && \
        apk del --purge build-base sqlite-dev

COPY . /app

CMD cd /app && bundle exec puma -C puma.rb
# CMD cd /app && bundle exec rackup -o 0.0.0.0
