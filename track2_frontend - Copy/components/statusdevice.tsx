"use client";
import { useEffect, useState } from "react";

interface DeviceStatus {
  online: boolean;
  connection?: {
    downlink: number;
    effectiveType: string;
    rtt: number;
  };
  battery?: {
    level: number;
    charging: boolean;
  };
}

export default function UseDeviceStatus({setStatus}: {setStatus: any}) {
  useEffect(() => {
    const updateConnection = () => {
      if ("connection" in navigator) {
        const connection = (navigator as any).connection;
        setStatus((prev: DeviceStatus) => ({
          ...prev,
          connection: {
            downlink: connection.downlink,
            effectiveType: connection.effectiveType,
            rtt: connection.rtt,
          },
        }));
      }
    };

    const updateBattery = async () => {
      if ("getBattery" in navigator) {
        const battery: any = await (navigator as any).getBattery();
        setStatus((prev: DeviceStatus) => ({
          ...prev,
          battery: {
            level: Math.round(battery.level * 100),
            charging: battery.charging,
          },
        }));

        battery.addEventListener("levelchange", () =>
          setStatus((prev: DeviceStatus) => ({
            ...prev,
            battery: {
              level: Math.round(battery.level * 100),
              charging: battery.charging,
            },
          }))
        );

        battery.addEventListener("chargingchange", () =>
          setStatus((prev: DeviceStatus) => ({
            ...prev,
            battery: {
              level: Math.round(battery.level * 100),
              charging: battery.charging,
            },
          }))
        );
      }
    };

    const updateOnlineStatus = () => {
      setStatus((prev: DeviceStatus) => ({ ...prev, online: navigator.onLine }));
    };

    // Initial call
    updateConnection();
    updateBattery();
    updateOnlineStatus();

    // Event listeners
    if ("connection" in navigator) {
      (navigator as any).connection.addEventListener("change", updateConnection);
    }
    window.addEventListener("online", updateOnlineStatus);
    window.addEventListener("offline", updateOnlineStatus);

    return () => {
      if ("connection" in navigator) {
        (navigator as any).connection.removeEventListener("change", updateConnection);
      }
      window.removeEventListener("online", updateOnlineStatus);
      window.removeEventListener("offline", updateOnlineStatus);
    };
  }, []);

  return null;
}