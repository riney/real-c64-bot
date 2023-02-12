#!/usr/bin/sh

psql -h postgres.local -U jack realc64bot -f db/schema.sql
