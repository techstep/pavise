-- table of malware sites for pavise

drop table if exists malware_sites;
create table malware_sites (
    id integer primary key autoincrement,
    site_url text not null,
    sha256_hash text not null,
    created datetime default current_timestamp,
    modified datetime default current_timestamp
);