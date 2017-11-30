CREATE TABLE `message_entry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `file_id` int(11) DEFAULT NULL,
  `content` text NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_user_id` (`user_id`),
  KEY `index_message_id` (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `message_entry` (`id`, `message_id`, `user_id`, `file_id`, `content`, `created_at`, `created_by`, `updated_at`, `updated_by`) VALUES
(1,	1,	1,	NULL,	'Foo',	'2017-09-26 11:59:04',	1,	'2017-09-26 11:59:04',	1),
(2,	1,	1,	NULL,	'!bot Bar',	'2017-09-26 11:59:09',	1,	'2017-09-26 11:59:09',	1),
(3,	1,	1,	NULL,	'!bot Foo',	'2017-09-26 12:09:46',	1,	'2017-09-26 12:09:46',	1),
(4,	1,	1,	NULL,	'!bot Foobar',	'2017-09-26 12:11:10',	1,	'2017-09-26 12:11:10',	1),
(5,	1,	1,	NULL,	'Lorem',	'2017-09-27 11:32:15',	1,	'2017-09-27 11:32:15',	1),
(6,	1,	1,	NULL,	'!bot Lipsum',	'2017-09-28 12:58:20',	1,	'2017-09-28 12:58:20',	1),
(7,	1,	1,	NULL,	'Lorem Lipsum',	'2017-10-01 10:23:26',	1,	'2017-10-01 10:23:26',	1);
