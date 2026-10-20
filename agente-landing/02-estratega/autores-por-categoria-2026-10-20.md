# Autor experto por categoría del blog · borrador para aprobación de Regina (propuesta 2026-10-20-3)

Fuente: /experts (JSON-LD, 31 expertas con cargo y especialidad). Regla: cada post lleva `author` Person (nombre, jobTitle, url a /experts) + leyenda visible "Revisado por …" + dateModified real. Se aplica DESPUÉS del freeze (lectura de Google de la semana 20-26 oct), por idioma, y se mide antes/después en Search Console. Donde una categoría no tiene especialista nativo en ese idioma, se usa la experta bilingüe más cercana (marcado con *).

| Categoría | EN | ES | PT |
|---|---|---|---|
| Salud / recién nacido / seguridad | Dr. Thanya Asse (Pediatrician, MD) | Dra. Stephane Fdz (Médico) · alt. Dra. Keyla Dguez | Kátia Regina Bueno (Médica Pediatra) |
| Sueño | Caryn Shender (Pediatric Sleep Consultant) · alt. Amaya Martínez | Amaya Martínez (Sleep Coach)* | Ester Alves (Especialista do Sono) · alt. Gabriella Demarque |
| Lactancia / alimentación / sólidos | Alicia Simpson (Nutritionist & IBCLC) | Mireya Siller (Consultora de Lactancia) · nutrición: Evelyn Flores | Jane del Corso (Enfermeira, Amamentação) · nutrição: Micheane Cruz |
| Físico / motor | Dr. Mercedes (Pediatric Physical Therapist) · alt. Sarah Rappenhagen (OT) | Isis Azcona (Fisioterapeuta) | Camila Blank (Especialista em Movimento) |
| Lenguaje | Delia Herrera (Speech & Language Pathologist) | Gimena Salazar (Lenguaje y Aprendizaje) | Lúcia Souza (Pedagoga e Musicoterapeuta) |
| Cognitivo / desarrollo / hitos | Sarah Rappenhagen (OT, neurodesarrollo) | Mily Saadia (Psicopedagoga) | Gabriela Azine (Psicóloga Perinatal e Neurociência) |
| Socioemocional | Sarah Rappenhagen* (no hay psicóloga EN en /experts) | Ángela Hernández (Psicóloga Clínica) · alt. Samantha Espino | Kássia Hübner (Psicóloga) · alt. Agda Ramos |
| Embarazo / posparto | Ale Conpeán (Fitness Coach, pregnancy & postpartum) | Evelyn Flores (Nutrición en embarazo) | Gabriela Azine (Perinatal) |

Pendientes para Regina: (1) ok al reparto o cambios; (2) confirmar que cada experta acepta aparecer como "revisado por" en artículos que no escribió (si no, la leyenda cambia a "Equipo de expertas de Kinedu, coordinado por …"); (3) si falta foto/bio pública de alguna, se usa la de /experts.
Implementación (Implementador, tras el freeze): script sobre los 3,416 posts que, según carpeta e idioma + categoría del post (kb-art-cat), inyecta el Person en el JSON-LD (author + reviewedBy) y una línea visible bajo el título. Sin tocar datePublished.
