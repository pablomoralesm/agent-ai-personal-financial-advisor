# Multi-Agent Architecture Plan

## 📋 **Current Situation Analysis**

### **Code Duplication Issues:**
1. **`agents/` folder**: Full multi-agent system with orchestrator, spending analyzer, goal planner, advisor
2. **`adk_web_agents/` folder**: Single simplified agent for ADK Web
3. **Different patterns**: Main agents use complex orchestration, ADK Web uses simple LLM agent

### **Existing Architecture Strengths:**
- **Comprehensive Multi-Agent System**: Well-designed orchestrator with specialized agents
- **Session State Sharing**: Agents communicate through `ctx.session.state`
- **Agent Delegation**: Using `AgentTool` pattern for agent-to-agent communication
- **MCP Integration**: All agents use MCP tools for database access
- **Factory Pattern**: Clean agent creation with factory functions
- **Streamlit Integration**: Working UI with real agent execution

### **Multi-Agent Goals:**
- Show agent collaboration and delegation
- Demonstrate session state sharing
- Implement agent-to-agent communication
- Show different agent specializations
- Support both Streamlit and ADK Web contexts
- Provide both educational and production orchestration patterns

## 🎯 **Proposed Solution: Hybrid Multi-Agent Architecture**

### **Core Principle: Context-Appropriate Orchestration**
- **Streamlit UI**: Procedural orchestrator only (educational focus)
- **ADK Web**: Both procedural and intelligent orchestrators (development focus)

### **Phase 1: Create Unified Agent Structure**

#### **1.1 Create `agents/unified/` Directory**
```
agents/unified/
├── __init__.py
├── base_agent.py              # Base classes and common patterns
├── agent_factory.py           # Factory for different deployment contexts
├── procedural_orchestrator.py # Educational orchestrator
├── intelligent_orchestrator.py # Production orchestrator
└── deployment_configs.py      # Configuration for different contexts
```

#### **1.2 Extract Common Agent Patterns**
- **Base Agent Classes**: Common initialization and MCP setup
- **Agent Communication**: Standardized session state sharing
- **Tool Integration**: Unified MCP tool configuration
- **Error Handling**: Consistent error patterns across agents

#### **1.3 Create Agent Factory System**
```python
class AgentFactory:
    @staticmethod
    def create_for_streamlit(mcp_server_path: str) -> ProceduralMultiAgentSystem
    @staticmethod
    def create_for_adk_web(mcp_server_path: str) -> HybridMultiAgentSystem
    @staticmethod
    def create_individual_agents(mcp_server_path: str) -> Dict[str, Agent]
    @staticmethod
    def create_orchestrator(orchestrator_type: str, mcp_server_path: str) -> Orchestrator
```

### **Phase 2: Implement Hybrid Multi-Agent ADK Web**

#### **2.1 Create Multi-Agent ADK Web Structure**
```
adk_web_agents/
├── __init__.py
├── multi_agent_system/
│   ├── __init__.py
│   ├── orchestrator_selector.py    # Choose between orchestrators
│   ├── procedural_orchestrator.py  # Educational orchestrator
│   ├── intelligent_orchestrator.py # Production orchestrator
│   ├── spending_analyzer.py        # ADK Web spending analyzer
│   ├── goal_planner.py             # ADK Web goal planner
│   └── advisor.py                  # ADK Web advisor
└── single_agent/                   # Keep simple single agent option
    └── financial_advisor/
        ├── __init__.py
        └── agent.py
```

#### **2.2 Implement Orchestrator Selection in ADK Web**
- **Orchestrator Selector**: Choose between procedural and intelligent
- **Agent Delegation**: Use `AgentTool` pattern for both orchestrators
- **Session State Sharing**: Implement shared context
- **Event Streaming**: Show agent collaboration in real-time

#### **2.3 Create ADK Web Orchestrator Selector**
```python
class OrchestratorSelector:
    def __init__(self, mcp_server_path: str):
        self.procedural = ProceduralOrchestrator(mcp_server_path)
        self.intelligent = IntelligentOrchestrator(mcp_server_path)
    
    def get_orchestrator(self, orchestrator_type: str):
        if orchestrator_type == "procedural":
            return self.procedural
        elif orchestrator_type == "intelligent":
            return self.intelligent
        else:
            raise ValueError(f"Unknown orchestrator type: {orchestrator_type}")
```

#### **2.4 Create Intelligent Orchestrator**
```python
class IntelligentOrchestrator(LlmAgent):
    def __init__(self, mcp_server_path: str):
        super().__init__(
            name="IntelligentOrchestrator",
            instruction="""
            You are an intelligent orchestrator that decides which agents to call
            based on the user's request. You have access to:
            - SpendingAnalyzerAgent: For spending analysis
            - GoalPlannerAgent: For goal planning  
            - AdvisorAgent: For financial advice
            
            Analyze the user's request and decide which agents to call and in what order.
            Provide reasoning for your decisions.
            """,
            tools=[
                AgentTool(agent=spending_analyzer.agent),
                AgentTool(agent=goal_planner.agent),
                AgentTool(agent=advisor.agent)
            ]
        )
```

### **Phase 3: Update Streamlit Integration (Procedural Only)**

#### **3.1 Refactor Streamlit to Use Procedural Orchestrator**
- **Update `streamlit_app.py`**: Use procedural orchestrator only
- **Maintain Existing Functionality**: Keep all current features
- **Add Multi-Agent Visualization**: Show agent collaboration
- **Enhanced Error Handling**: Better error reporting
- **Educational Focus**: Clear, transparent workflow

#### **3.2 Create Educational UI Components**
```python
def render_multi_agent_analysis():
    """Show real-time agent collaboration for educational purposes"""
    # Display agent status
    # Show session state sharing
    # Visualize agent delegation
    # Display orchestration progress
    # Show step-by-step workflow
```

#### **3.3 Enhanced Analysis Controls**
```python
def render_analysis_controls():
    """Enhanced analysis controls with educational focus"""
    st.markdown("## 🚀 Financial Analysis")
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Analysis Type",
        options=["Full Analysis", "Spending Only", "Goals Only", "Custom"]
    )
    
    # Custom workflow builder
    if analysis_type == "Custom":
        st.markdown("### 🔧 Custom Workflow")
        selected_agents = st.multiselect(
            "Select Agents",
            options=["Spending Analyzer", "Goal Planner", "Advisor"],
            default=["Spending Analyzer", "Goal Planner", "Advisor"]
        )
```

### **Phase 4: Testing and Validation**

#### **4.1 Multi-Agent Interaction Tests**
- **Agent Delegation Tests**: Verify agent-to-agent communication
- **Session State Tests**: Confirm data sharing between agents
- **Orchestration Tests**: Test both procedural and intelligent workflows
- **Context Switching Tests**: Verify both Streamlit and ADK Web work

#### **4.2 Integration Tests**
- **End-to-End Streamlit**: Full workflow with procedural orchestrator
- **End-to-End ADK Web**: Full workflow with both orchestrator types
- **Orchestrator Comparison**: Test both procedural and intelligent approaches
- **Cross-Platform Consistency**: Same results in both contexts

#### **4.3 Educational Value Tests**
- **Learning Progression**: Test educational value of procedural approach
- **Production Patterns**: Test intelligent orchestrator for real-world scenarios
- **User Experience**: Verify appropriate orchestration for each context

## 🔧 **Implementation Details**

### **Unified Agent Base Class**
```python
class UnifiedAgent:
    def __init__(self, name: str, mcp_server_path: str, deployment_context: str):
        self.name = name
        self.mcp_server_path = mcp_server_path
        self.deployment_context = deployment_context
        self.agent = self._create_agent()
    
    def _create_agent(self) -> LlmAgent:
        # Common agent creation logic
        # MCP tool setup
        # Context-specific configuration
```

### **Procedural Orchestrator (Educational)**
```python
class ProceduralOrchestrator(BaseAgent):
    """Educational orchestrator with clear, predictable workflow"""
    
    async def _run_async_impl(self, ctx):
        # Step 1: Spending Analysis
        yield ctx.create_event("📊 Starting spending analysis...", "progress")
        await self._spending_analyzer.analyze_customer_spending(ctx, customer_id)
        
        # Step 2: Goal Planning
        yield ctx.create_event("🎯 Starting goal planning...", "progress")
        await self._goal_planner.evaluate_goal_feasibility(ctx, customer_id)
        
        # Step 3: Advice Generation
        yield ctx.create_event("💡 Generating advice...", "progress")
        await self._advisor.provide_comprehensive_advice(ctx, customer_id)
        
        # Step 4: Summary
        yield ctx.create_event("✅ Analysis complete!", "completion")
```

### **Intelligent Orchestrator (Production)**
```python
class IntelligentOrchestrator(LlmAgent):
    """Production-style orchestrator with AI-powered decisions"""
    
    def __init__(self, mcp_server_path: str):
        super().__init__(
            name="IntelligentOrchestrator",
            instruction="""
            You are an intelligent orchestrator that decides which agents to call
            based on the user's request. Analyze the request and decide which agents
            to call and in what order. Provide reasoning for your decisions.
            """,
            tools=[
                AgentTool(agent=spending_analyzer.agent),
                AgentTool(agent=goal_planner.agent),
                AgentTool(agent=advisor.agent)
            ]
        )
```

### **Deployment Context Configuration**
```python
class DeploymentConfig:
    STREAMLIT = "streamlit"
    ADK_WEB = "adk_web"
    
    @staticmethod
    def get_config(context: str) -> Dict[str, Any]:
        configs = {
            "streamlit": {
                "orchestrator_type": "procedural",
                "use_runner": True,
                "session_service": "InMemorySessionService",
                "event_streaming": True,
                "educational_focus": True
            },
            "adk_web": {
                "orchestrator_type": "hybrid",  # Both available
                "use_runner": False,
                "session_service": "ADKWebSessionService", 
                "event_streaming": False,
                "educational_focus": False
            }
        }
        return configs.get(context, configs["streamlit"])
```

### **Orchestrator Selection Logic**
```python
class OrchestratorFactory:
    @staticmethod
    def create_orchestrator(context: str, orchestrator_type: str, mcp_server_path: str):
        if context == "streamlit":
            # Streamlit only supports procedural
            return ProceduralOrchestrator(mcp_server_path)
        elif context == "adk_web":
            # ADK Web supports both
            if orchestrator_type == "procedural":
                return ProceduralOrchestrator(mcp_server_path)
            elif orchestrator_type == "intelligent":
                return IntelligentOrchestrator(mcp_server_path)
            else:
                raise ValueError(f"Unknown orchestrator type: {orchestrator_type}")
```

## 📊 **Multi-Agent Interaction Patterns**

### **1. Agent Delegation Pattern**
```python
# Agent A delegates to Agent B
async def analyze_spending(self, ctx, customer_id: int):
    # SpendingAnalyzer delegates to Advisor
    advisor_result = await self.advisor.analyze_spending_patterns(ctx, customer_id)
    return advisor_result
```

### **2. Session State Sharing Pattern**
```python
# Agent A stores data, Agent B uses it
async def spending_analysis(self, ctx, customer_id: int):
    # Store analysis results
    ctx.session.state['spending_analysis'] = analysis_results

async def goal_planning(self, ctx, customer_id: int):
    # Use stored analysis
    spending_data = ctx.session.state.get('spending_analysis', {})
    # Use spending_data for goal planning
```

### **3. Orchestration Pattern**
```python
async def run_comprehensive_analysis(self, ctx, customer_id: int):
    # Step 1: Spending Analysis
    await self.spending_analyzer.analyze(ctx, customer_id)
    
    # Step 2: Goal Planning (uses spending data)
    await self.goal_planner.plan_goals(ctx, customer_id)
    
    # Step 3: Advisory (synthesizes all data)
    await self.advisor.provide_advice(ctx, customer_id)
```

## 🚀 **Benefits of Hybrid Architecture**

### **1. Educational Value**
- **Streamlit (Procedural)**: Clear, transparent multi-agent patterns for learning
- **ADK Web (Both)**: Advanced development with choice of orchestration
- **Learning Progression**: Natural path from simple to complex
- **Context-Appropriate**: Right tool for the right audience

### **2. Code Reuse**
- **Single Agent Implementation**: One set of agent logic
- **Shared MCP Configuration**: Common database access patterns
- **Unified Error Handling**: Consistent error management
- **Common Testing**: Shared test suites

### **3. Multi-Agent Demonstrations**
- **Agent Collaboration**: Show real agent-to-agent communication
- **Session State Sharing**: Demonstrate data flow between agents
- **Orchestration Logic**: Both procedural and intelligent workflows
- **Specialized Agents**: Each agent has distinct responsibilities

### **4. Deployment Flexibility**
- **Streamlit Integration**: Educational UI with procedural orchestrator
- **ADK Web Integration**: Development platform with both orchestrators
- **Production Ready**: Intelligent orchestrator for real-world scenarios
- **Testing Integration**: Comprehensive test coverage

### **5. Maintainability**
- **Single Source of Truth**: One implementation for each agent
- **Consistent Patterns**: Standardized agent development
- **Easy Updates**: Changes propagate to all contexts
- **Clear Separation**: Deployment vs. agent logic vs. orchestration

## 📋 **Migration Strategy**

### **Step 1: Create Unified Structure**
1. Create `agents/unified/` directory
2. Extract common patterns from existing agents
3. Create base classes and factory functions
4. Create both procedural and intelligent orchestrators
5. Maintain backward compatibility

### **Step 2: Implement ADK Web Hybrid System**
1. Create multi-agent ADK Web structure
2. Implement orchestrator selector
3. Create both procedural and intelligent orchestrators
4. Test agent delegation and session sharing
5. Verify ADK Web integration

### **Step 3: Update Streamlit (Procedural Only)**
1. Refactor Streamlit to use procedural orchestrator only
2. Add multi-agent visualization
3. Enhance educational features
4. Maintain existing functionality
5. Test end-to-end workflows

### **Step 4: Remove Duplication**
1. Remove duplicate agent code
2. Update imports and references
3. Clean up old files
4. Update documentation
5. Test both orchestration approaches

## 🎯 **Success Criteria**

### **Multi-Agent Interactions Demonstrated:**
- ✅ Agent-to-agent delegation working
- ✅ Session state sharing between agents
- ✅ Orchestration coordinating multiple agents
- ✅ Specialized agent responsibilities clear
- ✅ Real-time collaboration visible

### **Code Duplication Eliminated:**
- ✅ Single agent implementation
- ✅ Unified MCP configuration
- ✅ Shared error handling
- ✅ Common testing patterns

### **Hybrid Architecture Working:**
- ✅ Streamlit with procedural orchestrator (educational)
- ✅ ADK Web with both orchestrators (development)
- ✅ Orchestrator selection working in ADK Web
- ✅ Context-appropriate orchestration

### **Educational Value Achieved:**
- ✅ Clear learning progression from simple to complex
- ✅ Transparent multi-agent patterns in Streamlit
- ✅ Production patterns available in ADK Web
- ✅ Both approaches well-documented and tested

## 🔄 **Next Steps**

1. **Start with Phase 1**: Create unified agent structure with both orchestrators
2. **Implement ADK Web Hybrid System**: Show both orchestration approaches
3. **Update Streamlit**: Use procedural orchestrator only
4. **Test and Validate**: Ensure both approaches work
5. **Document and Clean Up**: Remove duplication and document both patterns

## 🎉 **Summary**

This hybrid architecture plan addresses the code duplication while achieving the multi-agent interaction goals, providing:

- **Educational Value**: Streamlit with clear, procedural orchestration
- **Production Value**: ADK Web with both orchestration approaches
- **Code Reuse**: Single agent implementations across contexts
- **Flexibility**: Right orchestration for the right use case
- **Learning Progression**: Natural path from simple to complex

The hybrid approach gives you the best of both worlds - educational clarity in Streamlit and production flexibility in ADK Web!
