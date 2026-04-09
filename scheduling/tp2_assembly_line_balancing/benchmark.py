"""
TP2 - Benchmarking: RC-ALBP Solver Performance Analysis

Run the CP-SAT solver on multiple realistic instances derived from RCPSP problems.
Collect results in a dataframe for analysis.

This script:
1. Loads RCPSP instances from PSPLib
2. Converts them to RC-ALBP problems
3. Solves with CP-SAT
4. Stores results for analysis
"""

import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional
from pathlib import Path

from discrete_optimization.generic_tools.cp_tools import ParametersCp

from scheduling.tp2_assembly_line_balancing.problem import RCALBPProblem, RCALBPSolution
from scheduling.tp2_assembly_line_balancing.utils import load_rcpsp_as_albp, visualize_interactive_flow
from scheduling.tp2_assembly_line_balancing.solutions import RCALBPCpSatSolver


def benchmark_instance(
    instance_name: str,
    nb_stations: int = 3,
    time_limit: int = 60,
    seed: int = 42,
) -> Dict:
    """
    Benchmark a single instance.

    Args:
        instance_name: RCPSP instance name (e.g., "j301_1")
        nb_stations: Number of assembly line stations
        time_limit: CP-SAT time limit in seconds
        seed: Random seed

    Returns:
        Dictionary with results
    """
    print(f"\n{'='*80}")
    print(f"Benchmarking: {instance_name} with {nb_stations} stations")
    print(f"{'='*80}\n")

    result = {
        "instance": instance_name,
        "nb_stations": nb_stations,
        "nb_tasks": 0,
        "nb_resources": 0,
        "nb_precedences": 0,
        "best_bound": None,
        "cycle_time": None,
        "solve_time": None,
        "is_optimal": False,
        "is_feasible": False,
        "is_valid": False,
        "status": "UNKNOWN",
    }

    try:
        # Load and convert problem
        problem = load_rcpsp_as_albp(
            instance_name=instance_name,
            nb_stations=nb_stations,
            seed=seed,
        )

        result["nb_tasks"] = problem.nb_tasks
        result["nb_resources"] = problem.nb_resources
        result["nb_precedences"] = len(problem.precedences)

        print(f"Problem: {problem.nb_tasks} tasks, {problem.nb_resources} resources")

        # Solve using discrete-optimization API
        start_time = time.time()
        cp_solver = RCALBPCpSatSolver(problem)
        params_cp = ParametersCp.default_cpsat()
        result_storage = cp_solver.solve(
            parameters_cp=params_cp,
            time_limit=time_limit,
            ortools_cpsat_solver_kwargs={"log_search_progress": True}
        )
        solve_time = time.time() - start_time

        result["solve_time"] = solve_time

        if len(result_storage) > 0:
            solution: RCALBPSolution = result_storage.get_best_solution()
            result["status"] = "SOLVED"
            result["cycle_time"] = solution.cycle_time
            result["is_feasible"] = True

            # Get best objective bound from solver
            best_bound = cp_solver.get_current_best_internal_objective_bound()
            result["best_bound"] = best_bound

            # Check validity
            is_valid = problem.satisfy(solution)
            result["is_valid"] = is_valid

            # Check if optimal using solver status
            from discrete_optimization.generic_tools.do_solver import StatusSolver
            result["is_optimal"] = (cp_solver.status_solver == StatusSolver.OPTIMAL)

            # Compute gap from best bound
            gap = solution.cycle_time - best_bound
            result["gap"] = gap
            result["gap_percent"] = (gap / best_bound * 100) if best_bound > 0 else 0

            print(f"\n[OK] Solution found!")
            print(f"  Cycle time: {solution.cycle_time}")
            print(f"  Best bound: {best_bound}")
            print(f"  Solve time: {solve_time:.2f}s")
            print(f"  Gap: {gap} ({result['gap_percent']:.1f}%)")
            print(f"  Optimal: {result['is_optimal']}")
            print(f"  Valid: {is_valid}")

        else:
            result["status"] = "NO_SOLUTION"
            print("\n[X] No solution found within time limit")

    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)
        print(f"\n[X] Error: {e}")

    return result


def run_benchmark_suite(
    instances: Optional[List[str]] = None,
    nb_stations_list: Optional[List[int]] = None,
    time_limit: int = 60,
    output_file: str = "benchmark_results.csv",
) -> pd.DataFrame:
    """
    Run benchmarks on multiple instances and configurations.

    Args:
        instances: List of RCPSP instance names to test
        nb_stations_list: List of station counts to test
        time_limit: CP-SAT time limit per instance
        output_file: CSV file to save results

    Returns:
        DataFrame with all results
    """
    # Default instances: small to medium RCPSP problems
    if instances is None:
        instances = [
            "j301_1", "j301_2", "j301_3",  # 30 tasks
            "j601_1", "j601_2",             # 60 tasks
            "j1201_1",                       # 120 tasks (large)
        ]

    if nb_stations_list is None:
        nb_stations_list = [2, 3, 4]

    print("\n" + "="*80)
    print("  RC-ALBP BENCHMARKING SUITE")
    print("="*80)
    print(f"\nInstances: {len(instances)}")
    print(f"Station configurations: {nb_stations_list}")
    print(f"Time limit: {time_limit}s per instance")
    print(f"Total runs: {len(instances) * len(nb_stations_list)}")

    results = []

    for instance in instances:
        for nb_stations in nb_stations_list:
            result = benchmark_instance(
                instance_name=instance,
                nb_stations=nb_stations,
                time_limit=time_limit,
            )
            results.append(result)

    # Create DataFrame
    df = pd.DataFrame(results)

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"\n{'='*80}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}\n")

    return df


def analyze_results(df: pd.DataFrame):
    """
    Analyze and print summary statistics from benchmark results.

    Args:
        df: DataFrame with benchmark results
    """
    print("\n" + "="*80)
    print("  BENCHMARK ANALYSIS")
    print("="*80 + "\n")

    # Overall statistics
    total_runs = len(df)
    solved = df[df['status'] == 'SOLVED'].shape[0]
    valid = df[df['is_valid'] == True].shape[0]
    optimal = df[df['is_optimal'] == True].shape[0]

    print(f"Total runs: {total_runs}")
    print(f"Solved: {solved}/{total_runs} ({solved/total_runs*100:.1f}%)")
    print(f"Valid: {valid}/{total_runs} ({valid/total_runs*100:.1f}%)")
    print(f"Optimal: {optimal}/{total_runs} ({optimal/total_runs*100:.1f}%)")

    # Solve time statistics
    solved_df = df[df['status'] == 'SOLVED']
    if not solved_df.empty:
        print(f"\nSolve Time Statistics:")
        print(f"  Mean: {solved_df['solve_time'].mean():.2f}s")
        print(f"  Median: {solved_df['solve_time'].median():.2f}s")
        print(f"  Min: {solved_df['solve_time'].min():.2f}s")
        print(f"  Max: {solved_df['solve_time'].max():.2f}s")

    # Gap statistics
    valid_df = df[df['is_valid'] == True]
    if not valid_df.empty and 'gap_percent' in valid_df.columns:
        print(f"\nOptimality Gap Statistics:")
        print(f"  Mean: {valid_df['gap_percent'].mean():.2f}%")
        print(f"  Median: {valid_df['gap_percent'].median():.2f}%")
        print(f"  Min: {valid_df['gap_percent'].min():.2f}%")
        print(f"  Max: {valid_df['gap_percent'].max():.2f}%")

    # Performance by instance size
    if 'nb_tasks' in df.columns:
        print(f"\nPerformance by Instance Size:")
        size_analysis = df.groupby('nb_tasks').agg({
            'is_valid': 'mean',
            'solve_time': 'mean',
            'gap_percent': 'mean'
        }).round(2)
        print(size_analysis)

    # Performance by number of stations
    if 'nb_stations' in df.columns:
        print(f"\nPerformance by Number of Stations:")
        station_analysis = df.groupby('nb_stations').agg({
            'is_valid': 'mean',
            'solve_time': 'mean',
            'gap_percent': 'mean'
        }).round(2)
        print(station_analysis)

    print("\n" + "="*80)


def plot_results(df: pd.DataFrame, save_plots: bool = True):
    """
    Create visualization plots from benchmark results.

    Args:
        df: DataFrame with benchmark results
        save_plots: If True, save plots to files
    """
    print("\n" + "="*80)
    print("  CREATING VISUALIZATION PLOTS")
    print("="*80 + "\n")

    # Filter valid solutions
    valid_df = df[df['is_valid'] == True].copy()

    if valid_df.empty:
        print("[!]  No valid solutions to plot!")
        return

    # Create figure with multiple subplots
    fig = plt.figure(figsize=(16, 10))

    # =========================================================================
    # 1. Cycle Time vs Number of Stations (Main Result!)
    # =========================================================================
    ax1 = plt.subplot(2, 3, 1)

    # Group by instance and nb_stations
    for instance in valid_df['instance'].unique():
        instance_data = valid_df[valid_df['instance'] == instance]
        if len(instance_data) > 0:
            # Sort by number of stations
            instance_data = instance_data.sort_values('nb_stations')

            ax1.plot(
                instance_data['nb_stations'],
                instance_data['cycle_time'],
                marker='o',
                linewidth=2,
                markersize=8,
                label=instance,
                alpha=0.7
            )

    ax1.set_xlabel('Number of Stations', fontsize=11)
    ax1.set_ylabel('Cycle Time', fontsize=11)
    ax1.set_title('Cycle Time vs Number of Stations', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=8, loc='best')
    ax1.grid(True, alpha=0.3)

    # =========================================================================
    # 2. Solve Time vs Number of Stations
    # =========================================================================
    ax2 = plt.subplot(2, 3, 2)

    # Average solve time per station count
    if 'nb_stations' in valid_df.columns and 'solve_time' in valid_df.columns:
        station_solve_time = valid_df.groupby('nb_stations')['solve_time'].agg(['mean', 'std'])

        ax2.bar(
            station_solve_time.index,
            station_solve_time['mean'],
            yerr=station_solve_time['std'],
            color='steelblue',
            alpha=0.7,
            capsize=5
        )

        ax2.set_xlabel('Number of Stations', fontsize=11)
        ax2.set_ylabel('Average Solve Time (s)', fontsize=11)
        ax2.set_title('Solve Time vs Stations', fontsize=12, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)

    # =========================================================================
    # 3. Optimality Rate vs Stations
    # =========================================================================
    ax3 = plt.subplot(2, 3, 3)

    if 'is_optimal' in valid_df.columns:
        optimal_rate = valid_df.groupby('nb_stations')['is_optimal'].mean() * 100

        bars = ax3.bar(
            optimal_rate.index,
            optimal_rate.values,
            color='lightgreen',
            alpha=0.7
        )

        # Add percentage labels
        for bar in bars:
            height = bar.get_height()
            ax3.text(
                bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}%',
                ha='center', va='bottom', fontsize=9
            )

        ax3.set_xlabel('Number of Stations', fontsize=11)
        ax3.set_ylabel('Optimality Rate (%)', fontsize=11)
        ax3.set_title('% of Optimal Solutions by Stations', fontsize=12, fontweight='bold')
        ax3.set_ylim(0, 110)
        ax3.grid(axis='y', alpha=0.3)

    # =========================================================================
    # 4. Instance Size Impact (Cycle Time vs Tasks)
    # =========================================================================
    ax4 = plt.subplot(2, 3, 4)

    if 'nb_tasks' in valid_df.columns:
        # Scatter plot: tasks vs cycle time, colored by stations
        for nb_stations in sorted(valid_df['nb_stations'].unique()):
            station_data = valid_df[valid_df['nb_stations'] == nb_stations]

            ax4.scatter(
                station_data['nb_tasks'],
                station_data['cycle_time'],
                s=100,
                alpha=0.6,
                label=f'{nb_stations} stations'
            )

        ax4.set_xlabel('Number of Tasks', fontsize=11)
        ax4.set_ylabel('Cycle Time', fontsize=11)
        ax4.set_title('Instance Size Impact', fontsize=12, fontweight='bold')
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)

    # =========================================================================
    # 5. Optimality Gap Distribution
    # =========================================================================
    ax5 = plt.subplot(2, 3, 5)

    if 'gap_percent' in valid_df.columns:
        gap_data = valid_df['gap_percent'].dropna()

        if len(gap_data) > 0:
            ax5.hist(gap_data, bins=20, color='coral', alpha=0.7, edgecolor='black')

            ax5.set_xlabel('Optimality Gap (%)', fontsize=11)
            ax5.set_ylabel('Frequency', fontsize=11)
            ax5.set_title('Distribution of Optimality Gaps', fontsize=12, fontweight='bold')
            ax5.grid(axis='y', alpha=0.3)

            # Add mean line
            mean_gap = gap_data.mean()
            ax5.axvline(mean_gap, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_gap:.1f}%')
            ax5.legend(fontsize=9)

    # =========================================================================
    # 6. Performance Summary Heatmap
    # =========================================================================
    ax6 = plt.subplot(2, 3, 6)

    if 'instance' in valid_df.columns and 'nb_stations' in valid_df.columns:
        # Create pivot table: instance x stations -> cycle_time
        pivot = valid_df.pivot_table(
            values='cycle_time',
            index='instance',
            columns='nb_stations',
            aggfunc='mean'
        )

        if not pivot.empty:
            im = ax6.imshow(pivot.values, cmap='YlOrRd', aspect='auto')

            ax6.set_xticks(np.arange(len(pivot.columns)))
            ax6.set_yticks(np.arange(len(pivot.index)))
            ax6.set_xticklabels(pivot.columns, fontsize=9)
            ax6.set_yticklabels(pivot.index, fontsize=9)

            # Add colorbar
            cbar = plt.colorbar(im, ax=ax6)
            cbar.set_label('Cycle Time', rotation=270, labelpad=20, fontsize=10)

            # Add text annotations
            for i in range(len(pivot.index)):
                for j in range(len(pivot.columns)):
                    if not np.isnan(pivot.values[i, j]):
                        text = ax6.text(
                            j, i, f'{pivot.values[i, j]:.0f}',
                            ha="center", va="center", color="black", fontsize=8
                        )

            ax6.set_xlabel('Number of Stations', fontsize=11)
            ax6.set_ylabel('Instance', fontsize=11)
            ax6.set_title('Cycle Time Heatmap', fontsize=12, fontweight='bold')

    plt.tight_layout()

    if save_plots:
        plot_path = Path(__file__).parent / 'benchmark_plots.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"[OK] Plots saved to: {plot_path}")

    plt.show()


def create_interactive_visualization(
    problem: RCALBPProblem,
    solution: RCALBPSolution,
    instance_name: str = "example"
):
    """
    Create and display interactive visualization of solution.

    Args:
        problem: Problem instance
        solution: Solution to visualize
        instance_name: Name for the instance
    """
    print(f"\n{'='*80}")
    print(f"  INTERACTIVE VISUALIZATION: {instance_name}")
    print(f"{'='*80}\n")

    print("Creating interactive assembly line flow animation...")
    print("   Use the time slider to see products flowing through stations!")
    print("   Watch resource usage and constraint violations in real-time.\n")

    try:
        visualize_interactive_flow(problem, solution)
        print("\n[Done] Visualization displayed\n")
    except Exception as e:
        print(f"[Error] Could not create visualization: {e}\n")


def main():
    """Main benchmarking function."""

    print("\n" + "="*80)
    print("  TP2 - RC-ALBP BENCHMARK")
    print("="*80)

    # Define test instances
    instances = [
        "j301_1", "j301_2", "j301_3",  # 30 tasks, 4 resources
    ]

    nb_stations_list = [2, 3, 4]
    time_limit = 30  # seconds per instance

    print("\n-> This script will:")
    print("   1. Load RCPSP instances from PSPLib")
    print("   2. Convert to RC-ALBP problems")
    print("   3. Solve with CP-SAT")
    print("   4. Collect results in DataFrame")
    print("   5. Save to CSV for analysis")

    print("\n[!]  IMPORTANT: Implement the solver in solutions.py first!")
    print("   The solver must be working to run this benchmark.\n")

    # Run benchmark
    try:
        df = run_benchmark_suite(
            instances=instances,
            nb_stations_list=nb_stations_list,
            time_limit=time_limit,
            output_file="tp2_benchmark_results.csv",
        )

        # Analyze results
        analyze_results(df)

        # Create plots
        plot_results(df, save_plots=True)

        # Display DataFrame
        print("\nDetailed Results:")
        print(df.to_string(index=False))

        # Create interactive visualization for one instance
        print("\n" + "="*80)
        print("  INTERACTIVE VISUALIZATION DEMO")
        print("="*80)

        # Pick first valid solution for interactive demo
        valid_results = df[df['is_valid'] == True]
        if len(valid_results) > 0:
            demo_row = valid_results.iloc[0]
            print(f"\nCreating interactive visualization for: {demo_row['instance']}")
            print(f"  Stations: {demo_row['nb_stations']}")
            print(f"  Cycle Time: {demo_row['cycle_time']}")

            try:
                # Recreate problem and solve
                demo_problem = load_rcpsp_as_albp(
                    instance_name=demo_row['instance'],
                    nb_stations=demo_row['nb_stations'],
                    seed=42
                )

                demo_solver = RCALBPCpSatSolver(demo_problem)
                params_cp = ParametersCp.default_cpsat()
                demo_result = demo_solver.solve(
                    parameters_cp=params_cp,
                    time_limit=time_limit,
                    ortools_cpsat_solver_kwargs={"log_search_progress": False}
                )

                if len(demo_result) > 0:
                    demo_solution = demo_result.get_best_solution()
                    create_interactive_visualization(
                        demo_problem,
                        demo_solution,
                        instance_name=demo_row['instance']
                    )
                else:
                    print("[!]  Could not recreate solution for demo")

            except Exception as e:
                print(f"[!]  Could not create interactive demo: {e}")
        else:
            print("\n[!]  No valid solutions available for interactive demo")

        print("\n*** Next steps:")
        print("   - Check benchmark_plots.png for visual analysis")
        print("   - Interactive visualization shows assembly line flow")
        print("   - Use time slider to explore different time periods")
        print("   - Red borders indicate constraint violations")
        print("   - Try different instance/station configurations")

    except ImportError:
        print("\n❌ Error: Solver not implemented yet!")
        print("   Complete solutions.py first, then run this benchmark.")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()