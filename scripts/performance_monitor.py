#!/usr/bin/env python3
"""
MACHO-GPT v3.4-mini 성능 모니터링 시스템
------------------------------------------
Samsung C&T Logistics · HVDC Project
파일명: performance_monitor.py

기능:
- 실시간 시스템 리소스 모니터링
- Streamlit 서비스 상태 확인
- MACHO-GPT 모듈 성능 측정
- KPI 임계값 알림
- JSON 형식 성능 보고서 생성
"""

from __future__ import annotations

import json
import time
import psutil
import requests
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
import subprocess
import threading
import signal
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
sys.path.append(str(Path(__file__).parent.parent))


@dataclass
class SystemMetrics:
    """시스템 성능 지표"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_sent: int
    network_recv: int


@dataclass
class ServiceStatus:
    """서비스 상태 정보"""
    port: int
    status: str  # "running", "stopped", "error"
    response_time: Optional[float]
    error_message: Optional[str]


@dataclass
class PerformanceReport:
    """성능 모니터링 보고서"""
    monitoring_start: str
    system_metrics: List[SystemMetrics]
    service_status: List[ServiceStatus]
    alerts: List[str]
    summary: Dict[str, Any]


class PerformanceMonitor:
    """
    MACHO-GPT v3.4-mini 성능 모니터링 클래스
    
    Mode: PRIME (실시간 모니터링)
    Confidence: ≥0.95 필요
    """
    
    def __init__(self, mode: str = "PRIME"):
        self.mode = mode
        self.confidence_threshold = 0.95
        self.is_running = False
        self.metrics_history: List[SystemMetrics] = []
        self.service_ports = [8505, 8508, 8509, 8510]
        self.kpi_thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'response_time': 5.0  # seconds
        }
        self.alerts: List[str] = []
        self.start_time = None
        
    def collect_system_metrics(self) -> SystemMetrics:
        """시스템 리소스 지표 수집"""
        try:
            # CPU 사용률
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 메모리 사용률
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 디스크 사용률 (Windows 호환)
            if os.name == 'nt':  # Windows
                disk = psutil.disk_usage('C:\\')
            else:  # Linux/Unix
                disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # 네트워크 I/O
            network = psutil.net_io_counters()
            network_sent = network.bytes_sent
            network_recv = network.bytes_recv
            
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                network_sent=network_sent,
                network_recv=network_recv
            )
        except Exception as e:
            print(f"⚠️ 시스템 지표 수집 실패: {e}")
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=0.0,
                memory_percent=0.0,
                disk_percent=0.0,
                network_sent=0,
                network_recv=0
            )
    
    def check_service_status(self, port: int) -> ServiceStatus:
        """개별 서비스 상태 확인"""
        try:
            start_time = time.time()
            response = requests.get(
                f"http://localhost:{port}", 
                timeout=5,
                allow_redirects=True
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                return ServiceStatus(
                    port=port,
                    status="running",
                    response_time=response_time,
                    error_message=None
                )
            else:
                return ServiceStatus(
                    port=port,
                    status="error",
                    response_time=response_time,
                    error_message=f"HTTP {response.status_code}"
                )
        except requests.ConnectionError:
            return ServiceStatus(
                port=port,
                status="stopped",
                response_time=None,
                error_message="Connection refused"
            )
        except requests.Timeout:
            return ServiceStatus(
                port=port,
                status="timeout",
                response_time=None,
                error_message="Request timeout"
            )
        except Exception as e:
            return ServiceStatus(
                port=port,
                status="error",
                response_time=None,
                error_message=str(e)
            )
    
    def check_all_services(self) -> List[ServiceStatus]:
        """모든 서비스 상태 일괄 확인"""
        service_statuses = []
        for port in self.service_ports:
            status = self.check_service_status(port)
            service_statuses.append(status)
        return service_statuses
    
    def check_kpi_thresholds(self, metrics: SystemMetrics, services: List[ServiceStatus]) -> List[str]:
        """KPI 임계값 확인 및 알림 생성"""
        alerts = []
        
        # 시스템 리소스 알림
        if metrics.cpu_percent > self.kpi_thresholds['cpu_percent']:
            alerts.append(f"🚨 HIGH CPU: {metrics.cpu_percent:.1f}% (임계값: {self.kpi_thresholds['cpu_percent']}%)")
        
        if metrics.memory_percent > self.kpi_thresholds['memory_percent']:
            alerts.append(f"🚨 HIGH MEMORY: {metrics.memory_percent:.1f}% (임계값: {self.kpi_thresholds['memory_percent']}%)")
        
        if metrics.disk_percent > self.kpi_thresholds['disk_percent']:
            alerts.append(f"🚨 HIGH DISK: {metrics.disk_percent:.1f}% (임계값: {self.kpi_thresholds['disk_percent']}%)")
        
        # 서비스 응답 시간 알림
        for service in services:
            if service.response_time and service.response_time > self.kpi_thresholds['response_time']:
                alerts.append(f"🚨 SLOW RESPONSE: Port {service.port} - {service.response_time:.2f}s")
            
            if service.status in ["stopped", "error", "timeout"]:
                alerts.append(f"🚨 SERVICE DOWN: Port {service.port} - {service.status}")
        
        return alerts
    
    def print_real_time_status(self, metrics: SystemMetrics, services: List[ServiceStatus]):
        """실시간 상태 출력"""
        print("\033[2J\033[H")  # 화면 클리어
        print("🤖 MACHO-GPT v3.4-mini 성능 모니터링 대시보드")
        print("=" * 60)
        print(f"📊 모니터링 시작: {self.start_time}")
        print(f"🕐 현재 시간: {metrics.timestamp}")
        print()
        
        # 시스템 리소스
        print("💻 시스템 리소스:")
        print(f"  CPU: {metrics.cpu_percent:6.1f}% {'🔴' if metrics.cpu_percent > 80 else '🟢'}")
        print(f"  MEM: {metrics.memory_percent:6.1f}% {'🔴' if metrics.memory_percent > 85 else '🟢'}")
        print(f"  DSK: {metrics.disk_percent:6.1f}% {'🔴' if metrics.disk_percent > 90 else '🟢'}")
        print()
        
        # 서비스 상태
        print("🚀 서비스 상태:")
        for service in services:
            status_icon = {
                "running": "🟢",
                "stopped": "🔴", 
                "error": "🟡",
                "timeout": "⚪"
            }.get(service.status, "❓")
            
            response_info = ""
            if service.response_time:
                response_info = f" ({service.response_time:.2f}s)"
            
            print(f"  Port {service.port}: {status_icon} {service.status.upper()}{response_info}")
        print()
        
        # 최근 알림
        if self.alerts:
            print("🚨 최근 알림:")
            for alert in self.alerts[-5:]:  # 최근 5개만 표시
                print(f"  {alert}")
        else:
            print("✅ 모든 시스템 정상 운영 중")
        
        print("\n" + "=" * 60)
        print("Ctrl+C를 눌러 모니터링을 중지하세요.")
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """요약 보고서 생성"""
        if not self.metrics_history:
            return {}
        
        # 평균 시스템 지표 계산
        total_metrics = len(self.metrics_history)
        avg_cpu = sum(m.cpu_percent for m in self.metrics_history) / total_metrics
        avg_memory = sum(m.memory_percent for m in self.metrics_history) / total_metrics
        avg_disk = sum(m.disk_percent for m in self.metrics_history) / total_metrics
        
        # 최대 사용률
        max_cpu = max(m.cpu_percent for m in self.metrics_history)
        max_memory = max(m.memory_percent for m in self.metrics_history)
        max_disk = max(m.disk_percent for m in self.metrics_history)
        
        return {
            "monitoring_duration": len(self.metrics_history),
            "average_metrics": {
                "cpu_percent": round(avg_cpu, 2),
                "memory_percent": round(avg_memory, 2),
                "disk_percent": round(avg_disk, 2)
            },
            "peak_metrics": {
                "cpu_percent": round(max_cpu, 2),
                "memory_percent": round(max_memory, 2),
                "disk_percent": round(max_disk, 2)
            },
            "total_alerts": len(self.alerts),
            "health_score": self.calculate_health_score(),
            "recommendations": self.generate_recommendations()
        }
    
    def calculate_health_score(self) -> float:
        """시스템 건강 점수 계산 (0-100)"""
        if not self.metrics_history:
            return 0.0
        
        # 평균 시스템 사용률 기반 점수 계산
        avg_cpu = sum(m.cpu_percent for m in self.metrics_history) / len(self.metrics_history)
        avg_memory = sum(m.memory_percent for m in self.metrics_history) / len(self.metrics_history)
        avg_disk = sum(m.disk_percent for m in self.metrics_history) / len(self.metrics_history)
        
        # 점수 계산 (낮은 사용률일수록 높은 점수)
        cpu_score = max(0, 100 - avg_cpu)
        memory_score = max(0, 100 - avg_memory)
        disk_score = max(0, 100 - avg_disk)
        alert_penalty = min(50, len(self.alerts) * 2)  # 알림당 2점 감점
        
        health_score = (cpu_score + memory_score + disk_score) / 3 - alert_penalty
        return round(max(0, min(100, health_score)), 2)
    
    def generate_recommendations(self) -> List[str]:
        """성능 개선 권장사항 생성"""
        recommendations = []
        
        if not self.metrics_history:
            return ["모니터링 데이터 부족"]
        
        avg_cpu = sum(m.cpu_percent for m in self.metrics_history) / len(self.metrics_history)
        avg_memory = sum(m.memory_percent for m in self.metrics_history) / len(self.metrics_history)
        avg_disk = sum(m.disk_percent for m in self.metrics_history) / len(self.metrics_history)
        
        if avg_cpu > 70:
            recommendations.append("CPU 사용률 최적화: 백그라운드 프로세스 확인 필요")
        
        if avg_memory > 80:
            recommendations.append("메모리 사용량 최적화: 메모리 리크 점검 권장")
        
        if avg_disk > 85:
            recommendations.append("디스크 공간 정리: 임시 파일 및 로그 정리 필요")
        
        if len(self.alerts) > 10:
            recommendations.append("시스템 안정성 개선: 임계값 조정 또는 리소스 확장 검토")
        
        if not recommendations:
            recommendations.append("시스템 상태 양호: 현재 설정 유지 권장")
        
        return recommendations
    
    def save_report(self, filename: Optional[str] = None) -> str:
        """성능 보고서 파일 저장"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_report_{timestamp}.json"
        
        report = PerformanceReport(
            monitoring_start=self.start_time or "Unknown",
            system_metrics=self.metrics_history,
            service_status=self.check_all_services(),
            alerts=self.alerts,
            summary=self.generate_summary_report()
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, ensure_ascii=False, indent=2)
        
        return filename
    
    def signal_handler(self, signum, frame):
        """종료 신호 처리"""
        print("\n\n🛑 모니터링 중지 중...")
        self.is_running = False
        
        # 최종 보고서 생성
        report_file = self.save_report()
        print(f"📊 성능 보고서 저장: {report_file}")
        
        # 요약 정보 출력
        summary = self.generate_summary_report()
        print("\n📋 모니터링 요약:")
        print(f"  - 모니터링 시간: {summary.get('monitoring_duration', 0)}회 측정")
        print(f"  - 시스템 건강 점수: {summary.get('health_score', 0)}/100")
        print(f"  - 총 알림 수: {summary.get('total_alerts', 0)}개")
        
        sys.exit(0)
    
    def start_monitoring(self, interval: int = 10):
        """실시간 모니터링 시작"""
        print("🚀 MACHO-GPT v3.4-mini 성능 모니터링 시작")
        print(f"📊 모니터링 간격: {interval}초")
        print("=" * 60)
        
        # 신호 핸들러 등록
        signal.signal(signal.SIGINT, self.signal_handler)
        
        self.is_running = True
        self.start_time = datetime.now().isoformat()
        
        try:
            while self.is_running:
                # 시스템 지표 수집
                metrics = self.collect_system_metrics()
                self.metrics_history.append(metrics)
                
                # 서비스 상태 확인
                services = self.check_all_services()
                
                # KPI 임계값 확인
                new_alerts = self.check_kpi_thresholds(metrics, services)
                self.alerts.extend(new_alerts)
                
                # 실시간 상태 출력
                self.print_real_time_status(metrics, services)
                
                # 대기
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)


def main():
    """성능 모니터링 메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MACHO-GPT v3.4-mini 성능 모니터링")
    parser.add_argument("--interval", type=int, default=10, help="모니터링 간격 (초)")
    parser.add_argument("--mode", default="PRIME", help="모니터링 모드")
    args = parser.parse_args()
    
    monitor = PerformanceMonitor(mode=args.mode)
    monitor.start_monitoring(interval=args.interval)


if __name__ == "__main__":
    main() 