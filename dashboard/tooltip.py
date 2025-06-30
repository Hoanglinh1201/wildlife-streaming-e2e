MAP_TOOLTIPS = {
    "html": """
        <div style='padding:12px; width:320px; background:#fefefe; border-radius:10px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.2); font-family:Arial, sans-serif;
                    font-size:14px; line-height:1.5; color:#2c3e50;'>
            <div style='font-weight:bold; font-size:22px; text-align:center; margin-bottom:8px;'>
                🐾 {species} ({gender})
            </div>
            <div><strong>Type:</strong> {type}</div>
            <div><strong>Age:</strong> {age} yrs</div>
            <div><strong>Born:</strong> {born_at}</div>
            <div><strong>Size:</strong> {length_cm} cm, {weight_kg} kg</div>
            <hr style="margin:10px 0;">
            <div style="font-size:13px;">
                <strong>Type:</strong> {tracker_type}<br>
                <strong>Battery:</strong> {tracker_battery}%<br>
                <strong>Status:</strong> {tracker_status}
            </div>
        </div>
    """,
    "style": {"backgroundColor": "transparent", "color": "#2c3e50"},
}
