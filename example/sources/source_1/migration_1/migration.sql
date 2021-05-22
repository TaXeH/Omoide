INSERT INTO realms (uuid, route, label) VALUES ('r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 'public', 'Public realm');
INSERT INTO permissions_realms (realm_uuid, value) VALUES ('r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 'public');
INSERT INTO themes (uuid, realm_uuid, route, label) VALUES ('t_ebe48c63-a395-48a3-a614-2bdf406e3b92', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 'farm', 'Farm theme');
INSERT INTO themes (uuid, realm_uuid, route, label) VALUES ('t_7682f95f-f488-4605-a839-ce6e7e6a3010', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 'gerbils', 'Gerbils theme');
INSERT INTO implicit_tags (uuid, theme_uuid, description) VALUES ('i_9f9c1784-caa0-4794-aeb7-40e5dcbec4d7', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'Do not show scary mouse');
INSERT INTO implicit_tags_values (implicit_tag_uuid, value) VALUES ('i_9f9c1784-caa0-4794-aeb7-40e5dcbec4d7', 'scary');
INSERT INTO synonyms (uuid, theme_uuid, description) VALUES ('s_e6d7d8f3-9cf7-494f-b376-ef056018ff58', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'Various mouse names');
INSERT INTO synonyms_values (synonym_uuid, value) VALUES ('s_e6d7d8f3-9cf7-494f-b376-ef056018ff58', 'mice');
INSERT INTO synonyms_values (synonym_uuid, value) VALUES ('s_e6d7d8f3-9cf7-494f-b376-ef056018ff58', 'gerbil');
INSERT INTO synonyms_values (synonym_uuid, value) VALUES ('s_e6d7d8f3-9cf7-494f-b376-ef056018ff58', 'mouse');
INSERT INTO groups (uuid, realm_uuid, theme_uuid, route, label, registered_on, registered_by, author, author_url, origin_url, comment, hierarchy) VALUES ('g_99156c03-ea14-410b-9f91-1b9d3b60d521', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'browney', 'Browney mouse', '2021-06-29', 'Igor Zyktin', '', '', '', '', 'gerbils');
INSERT INTO metas_to_groups (group_uuid, meta_uuid) VALUES ('g_99156c03-ea14-410b-9f91-1b9d3b60d521', 'm_4d309875-e04c-42d3-8b38-8e62b7d60695');
INSERT INTO metas_to_groups (group_uuid, meta_uuid) VALUES ('g_99156c03-ea14-410b-9f91-1b9d3b60d521', 'm_06f0bc2d-967e-49e1-87ca-317b607654ad');
INSERT INTO metas_to_groups (group_uuid, meta_uuid) VALUES ('g_99156c03-ea14-410b-9f91-1b9d3b60d521', 'm_d901bd0d-0395-45bf-b9f2-d6227cbd6d4a');
INSERT INTO metas_to_groups (group_uuid, meta_uuid) VALUES ('g_99156c03-ea14-410b-9f91-1b9d3b60d521', 'm_569bcfe7-f90b-4862-9bcf-c7891bc42386');
INSERT INTO groups (uuid, realm_uuid, theme_uuid, route, label, registered_on, registered_by, author, author_url, origin_url, comment, hierarchy) VALUES ('g_8ec32b6e-847a-4376-8f0e-d1499e8a5290', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'whitey', 'Whitey mouse', '2021-06-29', 'Igor Zyktin', '', '', '', '', 'gerbils');
INSERT INTO metas_to_groups (group_uuid, meta_uuid) VALUES ('g_8ec32b6e-847a-4376-8f0e-d1499e8a5290', 'm_76b43afb-0b61-4b86-93ae-105a6f614183');
INSERT INTO metas_to_groups (group_uuid, meta_uuid) VALUES ('g_8ec32b6e-847a-4376-8f0e-d1499e8a5290', 'm_e3ca9d94-e177-4b7c-914c-a25f060630fa');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_4d309875-e04c-42d3-8b38-8e62b7d60695', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'g_99156c03-ea14-410b-9f91-1b9d3b60d521', '', '', '', 'animal-1238228', 'jpg', 3048, 2164, 6.6, 625757, 0, 'image', 1, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_06f0bc2d-967e-49e1-87ca-317b607654ad', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'g_99156c03-ea14-410b-9f91-1b9d3b60d521', '', '', '', 'animal-1239130', 'jpg', 3392, 2336, 7.92, 803314, 0, 'image', 2, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_d901bd0d-0395-45bf-b9f2-d6227cbd6d4a', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'g_99156c03-ea14-410b-9f91-1b9d3b60d521', '', '', '', 'animal-1239134', 'jpg', 3192, 2336, 7.46, 917936, 0, 'image', 3, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_569bcfe7-f90b-4862-9bcf-c7891bc42386', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'g_99156c03-ea14-410b-9f91-1b9d3b60d521', '', '', '', 'animal-1239402', 'jpg', 3472, 2336, 8.11, 719538, 0, 'image', 4, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_76b43afb-0b61-4b86-93ae-105a6f614183', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'g_8ec32b6e-847a-4376-8f0e-d1499e8a5290', '', '', '', 'animal-1238237', 'jpg', 2728, 1992, 5.43, 635310, 0, 'image', 1, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_e3ca9d94-e177-4b7c-914c-a25f060630fa', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', 'g_8ec32b6e-847a-4376-8f0e-d1499e8a5290', '', '', '', 'animal-1238239', 'jpg', 2804, 2076, 5.82, 745793, 0, 'image', 2, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_72ac3567-dfac-4347-9096-050ac948d814', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'adorable-1239417', 'jpg', 3504, 2336, 8.19, 1448910, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_1264e6b1-6d88-40c5-aaf9-2e6d8d7201cf', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'animal-1238374', 'jpg', 3232, 2196, 7.1, 602224, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_799c84be-27ce-4fbe-9efb-908f4e1c7a70', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'animal-1238376', 'jpg', 2948, 2204, 6.5, 1348164, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_0313e057-960a-4a85-a7d1-bbdd101dd9f6', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'animal-1239221', 'jpg', 2732, 2016, 5.51, 1218300, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_2cf2f84d-a6ce-4dd1-96c5-9834d7e69ac1', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'domestic-animal-1584385', 'jpg', 3872, 2592, 10.04, 1783105, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_9cb0ec4a-8caf-429b-ac6b-af94e746f0e9', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'domestic-animal-1584388', 'jpg', 3303, 2211, 7.3, 1383076, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_0884d8bb-0993-4e54-87a6-46afa21ed3dd', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'gerbil-5195035', 'jpg', 3000, 3000, 9.0, 2096356, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_605408b6-14be-4d1f-806f-6a9f271ebfae', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'gerbil-716586', 'jpg', 4264, 3392, 14.46, 1187533, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_f076fff7-9881-485a-802f-d43275a6b49c', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'kulfoto_com', 'jpg', 630, 473, 0.3, 33191, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils');
INSERT INTO metas (uuid, realm_uuid, theme_uuid, group_uuid, path_to_content, path_to_preview, path_to_thumbnail, original_filename, original_extension, width, height, resolution, size, duration, type, ordering, registered_on, registered_by, author, author_url, origin_url, comment, signature, signature_type, previous, next, hierarchy) VALUES ('m_1d740c8b-9c41-4d80-bd35-f397551900df', 'r_45f0315d-7c11-4d4b-965f-7515e55b2d8a', 't_7682f95f-f488-4605-a839-ce6e7e6a3010', '', '', '', '', 'mouse-2204321', 'jpg', 3456, 2304, 7.96, 1523044, 0, 'image', 0, '2021-06-29', 'Igor Zyktin', '', '', '', '', '', '', '', '', 'gerbils')