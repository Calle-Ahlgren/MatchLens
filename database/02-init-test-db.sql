CREATE DATABASE matchlens_test;

\connect matchlens_test

\i /docker-entrypoint-initdb.d/01-init.sql