"use client";
import { useState } from "react";

export default function GetLocationClient({
  loc,
  setLoc,
}: {
  loc: { lat: number; lon: number } | null;
  setLoc: React.Dispatch<
    React.SetStateAction<{ lat: number; lon: number } | null>
  >;
}) {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const requestLocation = () => {
    if (!("geolocation" in navigator)) {
      setError("Browser does not support Geolocation API.");
      return;
    }
    setLoading(true);

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLoc({ lat: pos.coords.latitude, lon: pos.coords.longitude });
        setError(null);
        setLoading(false);
      },
      (err) => {
        setError(err.message || "Permission denied or error getting location");
        setLoading(false);
      },
      { enableHighAccuracy: true, timeout: 20000, maximumAge: 0 }
    );
  };

  return (
    <div>
      <button onClick={requestLocation} disabled={loading}>
        {loading ? "Requesting..." : "Get my location"}
      </button>

      {loc && (
        <div>
          <p>Latitude: {loc.lat}</p>
          <p>Longitude: {loc.lon}</p>
        </div>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
