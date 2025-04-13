SELECT e.event_id,
       e.title,
       e.date,
       v.name AS venue_name,
       COUNT(r.participant_id) AS registered_count,
       v.capacity,
       (COUNT(r.participant_id) * 1.0 / v.capacity) AS occupancy_ratio
FROM Event AS e
JOIN Venue AS v
    ON e.venue_id = v.venue_id
LEFT JOIN Registration AS r
    ON e.event_id = r.event_id
GROUP BY e.event_id, e.title, e.date, v.name, v.capacity;
