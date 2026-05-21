#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TokenSqueeze - 轻量级LLM Token智能压缩工具
Lightweight LLM Token Compression Tool

一个零依赖的Python工具，智能压缩命令行输出，为AI编码助手节省60-90%的Token消耗。
A zero-dependency Python tool that intelligently compresses command output,
saving 60-90% of token consumption for AI coding assistants.

Author: TokenSqueeze Team
License: MIT
Version: 1.0.0
"""

import sys
import re
import subprocess
import json
import os
import argparse
import time
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import tempfile
import hashlib

__version__ = "1.0.0"
__author__ = "TokenSqueeze Team"


@dataclass
class CompressionStats:
    """压缩统计信息"""
    original_tokens: int = 0
    compressed_tokens: int = 0
    command: str = ""
    timestamp: float = field(default_factory=time.time)
    
    @property
    def savings_percent(self) -> float:
        if self.original_tokens == 0:
            return 0.0
        return ((self.original_tokens - self.compressed_tokens) / self.original_tokens) * 100
    
    @property
    def savings_ratio(self) -> str:
        return f"{self.savings_percent:.1f}%"


class TokenEstimator:
    """Token估算器 - 基于字符数和常见Token化规则"""
    
    # 不同模型的平均token/字符比率
    MODEL_RATIOS = {
        'claude': 0.25,      # Claude系列
        'gpt4': 0.25,        # GPT-4
        'gpt3.5': 0.3,       # GPT-3.5
        'default': 0.25      # 默认
    }
    
    @classmethod
    def estimate(cls, text: str, model: str = 'default') -> int:
        """估算文本的Token数量"""
        ratio = cls.MODEL_RATIOS.get(model, cls.MODEL_RATIOS['default'])
        return int(len(text) * ratio)


class OutputCompressor:
    """输出压缩引擎"""
    
    def __init__(self):
        self.stats = CompressionStats()
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        return {
            'remove_ansi': True,
            'remove_progress_bars': True,
            'deduplicate_lines': True,
            'truncate_long_lines': 200,
            'max_output_lines': 500,
            'preserve_patterns': [
                r'error[:\s]', r'warning[:\s]', r'failed', r'success',
                r'✓', r'✗', r'PASS', r'FAIL'
            ]
        }
    
    def compress(self, text: str, command_type: str = 'generic') -> str:
        """压缩输出文本"""
        original = text
        
        # 1. 移除ANSI颜色代码
        if self.config['remove_ansi']:
            text = self._remove_ansi(text)
        
        # 2. 根据命令类型应用特定压缩规则
        text = self._apply_command_rules(text, command_type)
        
        # 3. 移除进度条
        if self.config['remove_progress_bars']:
            text = self._remove_progress_bars(text)
        
        # 4. 去重相似行
        if self.config['deduplicate_lines']:
            text = self._deduplicate_lines(text)
        
        # 5. 截断过长行
        text = self._truncate_lines(text)
        
        # 6. 限制总行数
        text = self._limit_lines(text)
        
        # 更新统计
        self.stats.original_tokens = TokenEstimator.estimate(original)
        self.stats.compressed_tokens = TokenEstimator.estimate(text)
        
        return text
    
    def _remove_ansi(self, text: str) -> str:
        """移除ANSI转义序列"""
        ansi_pattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_pattern.sub('', text)
    
    def _apply_command_rules(self, text: str, command_type: str) -> str:
        """应用命令特定规则"""
        rules = {
            'git': self._compress_git,
            'npm': self._compress_npm,
            'pytest': self._compress_pytest,
            'docker': self._compress_docker,
            'cargo': self._compress_cargo,
            'ls': self._compress_ls,
            'tree': self._compress_tree,
        }
        
        if command_type in rules:
            return rules[command_type](text)
        return text
    
    def _compress_git(self, text: str) -> str:
        """压缩git输出"""
        # 简化git status
        lines = text.split('\n')
        compressed = []
        
        for line in lines:
            # 跳过空行和提示信息
            if not line.strip() or 'use "git' in line.lower():
                continue
            # 简化文件状态行
            if line.startswith(' ') or line.startswith('\t'):
                line = line.strip()
            compressed.append(line)
        
        return '\n'.join(compressed)
    
    def _compress_npm(self, text: str) -> str:
        """压缩npm输出"""
        # 移除npm的冗长日志
        lines = text.split('\n')
        compressed = []
        
        for line in lines:
            # 跳过npm的进度和http日志
            if any(x in line for x in ['npm http', 'npm timing', '> ', '[......']):
                continue
            compressed.append(line)
        
        return '\n'.join(compressed)
    
    def _compress_pytest(self, text: str) -> str:
        """压缩pytest输出"""
        lines = text.split('\n')
        compressed = []
        in_traceback = False
        
        for line in lines:
            # 保留测试结果摘要
            if any(x in line for x in ['passed', 'failed', 'error', 'PASSED', 'FAILED']):
                compressed.append(line)
                continue
            
            # 简化traceback
            if 'Traceback' in line:
                in_traceback = True
                compressed.append('[Traceback truncated...]')
                continue
            
            if in_traceback and line.strip() and not line.startswith(' '):
                in_traceback = False
            
            if not in_traceback:
                compressed.append(line)
        
        return '\n'.join(compressed)
    
    def _compress_docker(self, text: str) -> str:
        """压缩docker输出"""
        lines = text.split('\n')
        compressed = []
        
        for line in lines:
            # 简化容器列表
            if line.startswith('CONTAINER'):
                compressed.append(line)
                continue
            # 移除pull进度
            if 'Pulling' in line and 'complete' not in line.lower():
                continue
            compressed.append(line)
        
        return '\n'.join(compressed)
    
    def _compress_cargo(self, text: str) -> str:
        """压缩cargo输出"""
        lines = text.split('\n')
        compressed = []
        
        for line in lines:
            # 保留编译结果，跳过进度
            if 'Compiling' in line and '=>' not in line:
                continue
            if 'Finished' in line or 'error' in line.lower() or 'warning' in line.lower():
                compressed.append(line)
                continue
            compressed.append(line)
        
        return '\n'.join(compressed)
    
    def _compress_ls(self, text: str) -> str:
        """压缩ls输出"""
        lines = text.split('\n')
        if len(lines) > 20:
            # 大量文件时只显示摘要
            return f"[{len(lines)} items]\n" + '\n'.join(lines[:10]) + "\n..."
        return text
    
    def _compress_tree(self, text: str) -> str:
        """压缩tree输出"""
        lines = text.split('\n')
        if len(lines) > 50:
            # 限制深度
            return '\n'.join(lines[:30]) + f"\n... ({len(lines) - 30} more lines)"
        return text
    
    def _remove_progress_bars(self, text: str) -> str:
        """移除进度条"""
        # 匹配各种进度条格式
        patterns = [
            r'\[\s*[=#\-]+\s*\]\s*\d+%\s*\d*/\d*\s*',  # [====>] 50% 1/2
            r'\d+%\s*\|[^\n]*\|',  # 50% |████    |
            r'[#\*\.]\s*\d+%',  # **** 50%
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text)
        
        return text
    
    def _deduplicate_lines(self, text: str) -> str:
        """去重相似行"""
        lines = text.split('\n')
        if len(lines) < 10:
            return text
        
        compressed = []
        prev_line = None
        duplicate_count = 0
        
        for line in lines:
            # 检查是否为重复行（忽略数字差异）
            line_pattern = re.sub(r'\d+', 'N', line)
            prev_pattern = re.sub(r'\d+', 'N', prev_line) if prev_line else None
            
            if line_pattern == prev_pattern and line_pattern.strip():
                duplicate_count += 1
            else:
                if duplicate_count > 0:
                    compressed.append(f"... ({duplicate_count} similar lines)")
                    duplicate_count = 0
                compressed.append(line)
                prev_line = line
        
        if duplicate_count > 0:
            compressed.append(f"... ({duplicate_count} similar lines)")
        
        return '\n'.join(compressed)
    
    def _truncate_lines(self, text: str) -> str:
        """截断过长行"""
        lines = text.split('\n')
        max_len = self.config['truncate_long_lines']
        
        compressed = []
        for line in lines:
            if len(line) > max_len:
                line = line[:max_len] + " ... [truncated]"
            compressed.append(line)
        
        return '\n'.join(compressed)
    
    def _limit_lines(self, text: str) -> str:
        """限制总行数"""
        lines = text.split('\n')
        max_lines = self.config['max_output_lines']
        
        if len(lines) > max_lines:
            return '\n'.join(lines[:max_lines//2]) + \
                   f"\n\n... [{len(lines) - max_lines} lines truncated] ...\n\n" + \
                   '\n'.join(lines[-max_lines//2:])
        
        return text


class CommandRunner:
    """命令执行器"""
    
    def __init__(self):
        self.compressor = OutputCompressor()
    
    def detect_command_type(self, command: List[str]) -> str:
        """检测命令类型"""
        if not command:
            return 'generic'
        
        cmd = command[0].lower()
        
        # 移除常见前缀
        if cmd in ['python', 'python3', 'npx', 'yarn', 'pnpm']:
            if len(command) > 1:
                cmd = command[1].lower()
        
        type_map = {
            'git': 'git',
            'npm': 'npm',
            'yarn': 'npm',
            'pnpm': 'npm',
            'pytest': 'pytest',
            'python': 'pytest',
            'docker': 'docker',
            'docker-compose': 'docker',
            'cargo': 'cargo',
            'ls': 'ls',
            'tree': 'tree',
            'find': 'tree',
        }
        
        return type_map.get(cmd, 'generic')
    
    def run(self, command: List[str], capture_output: bool = True) -> Tuple[int, str, CompressionStats]:
        """执行命令并压缩输出"""
        self.compressor.stats.command = ' '.join(command)
        
        try:
            # 执行命令
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=300,
                encoding='utf-8',
                errors='replace'
            )
            
            # 合并stdout和stderr
            output = result.stdout or ""
            if result.stderr:
                output += "\n" + result.stderr if output else result.stderr
            
            # 检测命令类型并压缩
            cmd_type = self.detect_command_type(command)
            compressed = self.compressor.compress(output, cmd_type)
            
            return result.returncode, compressed, self.compressor.stats
            
        except subprocess.TimeoutExpired:
            return -1, "Error: Command timed out after 5 minutes", self.compressor.stats
        except FileNotFoundError:
            return 127, f"Error: Command not found: {command[0]}", self.compressor.stats
        except Exception as e:
            return 1, f"Error: {str(e)}", self.compressor.stats


class StatsManager:
    """统计管理器"""
    
    def __init__(self):
        self.data_dir = os.path.expanduser('~/.tokensqueeze')
        self.stats_file = os.path.join(self.data_dir, 'stats.json')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_stats(self, stats: CompressionStats):
        """保存统计"""
        data = self.load_all_stats()
        data['sessions'].append({
            'command': stats.command,
            'original_tokens': stats.original_tokens,
            'compressed_tokens': stats.compressed_tokens,
            'savings_percent': stats.savings_percent,
            'timestamp': stats.timestamp
        })
        
        # 更新总计
        data['total']['commands'] += 1
        data['total']['original_tokens'] += stats.original_tokens
        data['total']['compressed_tokens'] += stats.compressed_tokens
        
        with open(self.stats_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_all_stats(self) -> Dict:
        """加载所有统计"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'total': {
                'commands': 0,
                'original_tokens': 0,
                'compressed_tokens': 0
            },
            'sessions': []
        }
    
    def get_summary(self) -> str:
        """获取统计摘要"""
        data = self.load_all_stats()
        total = data['total']
        
        if total['original_tokens'] == 0:
            return "No statistics available yet."
        
        savings = ((total['original_tokens'] - total['compressed_tokens']) 
                   / total['original_tokens']) * 100
        
        return f"""
📊 TokenSqueeze Statistics
═══════════════════════════════════════
Total commands processed: {total['commands']}
Original tokens: {total['original_tokens']:,}
Compressed tokens: {total['compressed_tokens']:,}
Tokens saved: {total['original_tokens'] - total['compressed_tokens']:,}
Average savings: {savings:.1f}%
"""


class MCPHandler:
    """MCP协议处理器 - 为AI Agent提供接口"""
    
    def __init__(self):
        self.runner = CommandRunner()
    
    def handle_request(self, request: Dict) -> Dict:
        """处理MCP请求"""
        method = request.get('method', '')
        params = request.get('params', {})
        
        if method == 'squeeze':
            command = params.get('command', [])
            returncode, output, stats = self.runner.run(command)
            
            return {
                'output': output,
                'returncode': returncode,
                'stats': {
                    'original_tokens': stats.original_tokens,
                    'compressed_tokens': stats.compressed_tokens,
                    'savings_percent': stats.savings_percent
                }
            }
        
        elif method == 'stats':
            manager = StatsManager()
            return {'summary': manager.get_summary()}
        
        return {'error': 'Unknown method'}


def create_cli_parser() -> argparse.ArgumentParser:
    """创建CLI参数解析器"""
    parser = argparse.ArgumentParser(
        prog='tokensqueeze',
        description='TokenSqueeze - 轻量级LLM Token智能压缩工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  tokensqueeze git status              # 压缩git状态输出
  tokensqueeze npm test                # 压缩npm测试输出
  tokensqueeze pytest -v               # 压缩pytest输出
  tokensqueeze --stats                 # 查看统计信息
  tokensqueeze --version               # 显示版本
        """
    )
    
    parser.add_argument(
        'command',
        nargs=argparse.REMAINDER,
        help='要执行的命令及其参数'
    )
    
    parser.add_argument(
        '--stats', '-s',
        action='store_true',
        help='显示统计信息'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help='显示版本信息'
    )
    
    parser.add_argument(
        '--mcp',
        action='store_true',
        help='以MCP服务器模式运行'
    )
    
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='不保存统计信息'
    )
    
    return parser


def main():
    """主入口函数"""
    parser = create_cli_parser()
    args = parser.parse_args()
    
    # 显示版本
    if args.version:
        print(f"TokenSqueeze v{__version__}")
        print(f"Author: {__author__}")
        print("License: MIT")
        return 0
    
    # 显示统计
    if args.stats:
        manager = StatsManager()
        print(manager.get_summary())
        return 0
    
    # MCP模式
    if args.mcp:
        handler = MCPHandler()
        print("TokenSqueeze MCP Server started", file=sys.stderr)
        
        for line in sys.stdin:
            try:
                request = json.loads(line)
                response = handler.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                print(json.dumps({'error': 'Invalid JSON'}), flush=True)
            except Exception as e:
                print(json.dumps({'error': str(e)}), flush=True)
        
        return 0
    
    # 执行命令
    if not args.command:
        parser.print_help()
        return 1
    
    runner = CommandRunner()
    returncode, output, stats = runner.run(args.command)
    
    # 打印压缩后的输出
    print(output)
    
    # 打印统计信息（stderr，不干扰正常输出）
    if stats.original_tokens > 0:
        print(
            f"\n[TokenSqueeze: {stats.original_tokens} → {stats.compressed_tokens} tokens "
            f"({stats.savings_ratio} saved)]",
            file=sys.stderr
        )
    
    # 保存统计
    if not args.no_save:
        manager = StatsManager()
        manager.save_stats(stats)
    
    return returncode


if __name__ == '__main__':
    sys.exit(main())
