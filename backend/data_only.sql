--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: flats; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.flats (id, location, price, image, tower_name, floor, is_booked, amenities, flat_number, flat_type) FROM stdin;
13	Hebbal,Bengluru	25000	https://tse4.mm.bing.net/th/id/OIP.wHwUc5Q57OxyZ9g86rIGOwHaEc?rs=1&pid=ImgDetMain&o=7&rm=3	2b	2	t	["Pool"," Parking"]	201	2BHK
14	Mysore	30000	https://tse1.mm.bing.net/th/id/OIP.SV1Xzf6FaGgDh9rVkKEmEQHaFI?rs=1&pid=ImgDetMain&o=7&rm=3	1B	4	t	["Car parking"," Gym"]	304	3BHK
12	Bengaluru	12000	https://tse4.mm.bing.net/th/id/OIP.ZUpClsWGaOGqSXuAyaDlSQHaE7?rs=1&pid=ImgDetMain&o=7&rm=3	2A	1	t	["Parking"]	101	1BHK
15	Malleshwaram,Bengaluru	25000	https://5.imimg.com/data5/SELLER/Default/2021/12/XI/YZ/PV/51665645/appartments-flats-interior-design-1000x1000.jpg	2B	2	t	["Parking"," Pool"," Gym"]	405	2BHK
1	Bengaluru	20000	https://plus.unsplash.com/premium_photo-1676823553207-758c7a66e9bb?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D	1A	5	t	["Pool"," Gym"," Parking"]	101	1BHK
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, name, email, password, role) FROM stdin;
2	Rakshitha	rakshithag227@gmail.com	scrypt:32768:8:1$xvssYSdBrorZ4tXT$0d4081c8f7e63069c6203d7b131c26113e6e2dfbd36c546f22ce81a1c7f0eb65f342f6063c0ae7835883f40c3fa5a19546009db032339c648dd621db4275f0ed	user
13	ram	ram@gmail.com	scrypt:32768:8:1$D4fHrmpz26ed78BD$7d7b4234bc875b53689823ae0db77660d5080fa77bf4036539b2959c78a8facaf87b135257930e542f467dd3379271a4fd82ecb6d48084fa06d3b9a53b178835	user
49	rakshi	rakshi@gmail.com	scrypt:32768:8:1$gybGIFNerS6t3dnM$7bbc0fd158bc7cf49fcf112706a83ce5b64c8ab84d7cb8283f82930369907c4a4562460acf57e03dba249e1ec0fc6e2b2e5fb84dd7816ea42f7a109b32644a1b	user
50	admin	admin@gmail.com	scrypt:32768:8:1$ACt2e9gym0CuBE2d$a8b3640dd612d53f53ccebeaef7cfa2cf2ba636473d4e45041f113a87fbee66881f68138232fdd97e53396d35f8622806bc77e3425266734d35679614b4428fb	admin
51	abc	ac@gmail.com	scrypt:32768:8:1$bUGhZi6J0u4oqiSD$408ac4bce3f7c8c21eb3eb4e6ae4af15968329f2dc7f6a58752eca7b65f3413ddbda1b13aa24c68187151c2748e7a4eb71e0e14b9fb8aec8356c39aab68f88e6	user
52	user	user@gmail.com	scrypt:32768:8:1$Zin5SAJKhWT0sMQC$b03eab7a4f9efc4e16f382a5eb71209ce2d9235f9d758f3e43b5db0eab9e7c13f8503dce89cdfd83c99de360e8655e33eb0d81f2e6a267c4a1137dcc1cef4ac6	user
\.


--
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookings (id, user_id, flat_id, booked_at, status) FROM stdin;
79	2	12	2026-03-08 10:20:11.58947	approved
80	2	15	2026-03-08 10:32:37.342727	approved
\.


--
-- Name: bookings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bookings_id_seq', 80, true);


--
-- Name: flats_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.flats_id_seq', 15, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 52, true);


--
-- PostgreSQL database dump complete
--

