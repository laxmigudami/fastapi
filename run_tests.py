"""
Test Runner Script for Siemens Energy API Testing Framework
Provides easy command-line interface for running different test suites
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Execute a command and handle errors"""
    print(f"\n{'='*80}")
    print(f"🚀 {description}")
    print(f"{'='*80}\n")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {description} failed with exit code {e.returncode}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Siemens Energy API Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests
  python run_tests.py --all
  
  # Run only manual tests
  python run_tests.py --manual
  
  # Run generated tests
  python run_tests.py --generated
  
  # Run with coverage
  python run_tests.py --all --coverage
  
  # Run specific markers
  python run_tests.py --markers smoke
  
  # Run with parallel execution
  python run_tests.py --all --parallel
  
  # Run specific test file
  python run_tests.py --file tests/test_posts.py
  
  # Generate HTML report
  python run_tests.py --all --html-report
        """
    )
    
    # Test scope options
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--all', action='store_true', help='Run all tests (manual + generated)')
    scope.add_argument('--manual', action='store_true', help='Run only manual tests')
    scope.add_argument('--generated', action='store_true', help='Run only generated tests')
    scope.add_argument('--file', type=str, help='Run specific test file')
    
    # Test markers
    parser.add_argument('--markers', type=str, help='Run tests with specific markers (e.g., smoke, regression)')
    
    # Execution options
    parser.add_argument('--parallel', action='store_true', help='Run tests in parallel')
    parser.add_argument('--workers', type=int, default=None, help='Number of parallel workers')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet output')
    
    # Reporting options
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--html-report', action='store_true', help='Generate HTML test report')
    parser.add_argument('--allure', action='store_true', help='Generate Allure report')
    parser.add_argument('--junit', action='store_true', help='Generate JUnit XML report')
    
    # Environment
    parser.add_argument('--env', type=str, default='dev', choices=['dev', 'staging', 'prod'], 
                       help='Environment to run tests against')
    
    # Other options
    parser.add_argument('--failfast', '-x', action='store_true', help='Stop on first failure')
    parser.add_argument('--last-failed', '--lf', action='store_true', help='Run only last failed tests')
    parser.add_argument('--failed-first', '--ff', action='store_true', help='Run failed tests first')
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd_parts = ['pytest']
    
    # Determine test paths
    if args.all:
        cmd_parts.append('tests/ generator/generated-tests/')
    elif args.manual:
        cmd_parts.append('tests/')
    elif args.generated:
        cmd_parts.append('generator/generated-tests/')
    elif args.file:
        cmd_parts.append(args.file)
    else:
        # Default to manual tests
        cmd_parts.append('tests/')
    
    # Markers
    if args.markers:
        cmd_parts.append(f'-m {args.markers}')
    
    # Verbosity
    if args.verbose:
        cmd_parts.append('-vv')
    elif args.quiet:
        cmd_parts.append('-q')
    else:
        cmd_parts.append('-v')
    
    # Parallel execution
    if args.parallel:
        workers = args.workers if args.workers else 'auto'
        cmd_parts.append(f'-n {workers}')
    
    # Coverage
    if args.coverage:
        cmd_parts.extend([
            '--cov=app',
            '--cov-report=html',
            '--cov-report=term-missing',
            '--cov-report=xml'
        ])
    
    # HTML Report
    if args.html_report:
        os.makedirs('reports', exist_ok=True)
        cmd_parts.extend([
            '--html=reports/pytest-report.html',
            '--self-contained-html'
        ])
    
    # JUnit XML
    if args.junit:
        os.makedirs('reports', exist_ok=True)
        cmd_parts.append('--junitxml=reports/junit.xml')
    
    # Allure
    if args.allure:
        os.makedirs('allure-results', exist_ok=True)
        cmd_parts.append('--alluredir=allure-results')
    
    # Fail fast
    if args.failfast:
        cmd_parts.append('-x')
    
    # Last failed
    if args.last_failed:
        cmd_parts.append('--lf')
    
    # Failed first
    if args.failed_first:
        cmd_parts.append('--ff')
    
    # Load environment variables
    env_file = f'config/{args.env}.env'
    if os.path.exists(env_file):
        print(f"\n📋 Loading environment: {args.env}")
        from dotenv import load_dotenv
        load_dotenv(env_file)
    else:
        print(f"\n⚠️  Warning: Environment file {env_file} not found")
    
    # Build final command
    cmd = ' '.join(cmd_parts)
    
    # Run tests
    print(f"\n{'='*80}")
    print(f"🧪 Siemens Energy API Testing Framework")
    print(f"{'='*80}")
    print(f"Environment: {args.env}")
    print(f"Command: {cmd}")
    
    success = run_command(cmd, "Running Tests")
    
    # Generate Allure report if requested
    if args.allure and success:
        allure_cmd = "allure generate allure-results --clean -o allure-report"
        run_command(allure_cmd, "Generating Allure Report")
        print("\n📊 Allure report generated at: allure-report/index.html")
    
    # Summary
    print(f"\n{'='*80}")
    if success:
        print("✅ Tests completed successfully!")
    else:
        print("❌ Tests failed. Check the output above for details.")
        sys.exit(1)
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
