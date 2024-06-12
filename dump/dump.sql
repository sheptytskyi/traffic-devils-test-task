--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6
-- Dumped by pg_dump version 14.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, email, hashed_password, is_active, is_verified, role) FROM stdin;
3	user3@example.com	$argon2id$v=19$m=65536,t=3,p=4$XNy6yoEb46HRTij+Im/dlQ$GuFhNLsB7ZXYzFXrJARaA9nljaJtjCpx3gFgf9RYm+Q	t	f	user
4	user4@example.com	$argon2id$v=19$m=65536,t=3,p=4$02Jj04Rq2R28KcG2lcUDDA$CyOAmoJ8gJf2Qp6eh4Hj4sd4leqt6Qez75Io23YU9p0	t	f	user
5	user5@example.com	$argon2id$v=19$m=65536,t=3,p=4$D77qgPJvzX+mh5znDFrvxA$Wj8Y3LBqsTkgUw+Q2MwW3lYaqqAVAe/WC3DPvAOOdIA	t	f	user
1	user@example.com	$argon2id$v=19$m=65536,t=3,p=4$1pfCksqzEJHFZI3dbea+bQ$B3CP2G0csp/nk85w/feV/v1dlCH+zv0wCqxYpWOLR8k	t	f	admin
2	user2@example.com	$argon2id$v=19$m=65536,t=3,p=4$sU9g2MGsa7oiUAY4XJoaSg$A7Ccda8z9UPAb4UUDRjqfP939Al2nkZOCq/7IK7b3MI	t	f	manager
\.


--
-- Data for Name: telegram_response; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.telegram_response (id, message_id, from_id, from_is_bot, from_first_name, from_last_name, from_username, chat_id, chat_first_name, chat_last_name, chat_username, chat_type, date, text, user_id) FROM stdin;
1	136	6970441387	t	test_work_bot_bwn	\N	my_super_puper_cute_bot	848484880	ᴅɪᴍᴀ	ꜱʜᴇᴘᴛʏᴛꜱᴋʏɪ	dmytro_sheptytskyi	private	2024-06-12 16:18:14+00	test_message_1	3
2	137	6970441387	t	test_work_bot_bwn	\N	my_super_puper_cute_bot	848484880	ᴅɪᴍᴀ	ꜱʜᴇᴘᴛʏᴛꜱᴋʏɪ	dmytro_sheptytskyi	private	2024-06-12 16:18:45+00	test_message_2	4
3	138	6970441387	t	test_work_bot_bwn	\N	my_super_puper_cute_bot	848484880	ᴅɪᴍᴀ	ꜱʜᴇᴘᴛʏᴛꜱᴋʏɪ	dmytro_sheptytskyi	private	2024-06-12 16:19:05+00	test_message_2	5
\.


--
-- Data for Name: user_manager; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_manager (id, user_id) FROM stdin;
1	2
\.


--
-- Data for Name: users_user_managers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_user_managers (id, user_id, manager_id) FROM stdin;
1	3	1
2	4	1
\.


--
-- Name: telegram_response_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.telegram_response_id_seq', 3, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 5, true);


--
-- Name: user_manager_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_manager_id_seq', 2, true);


--
-- Name: users_user_managers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_managers_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--

