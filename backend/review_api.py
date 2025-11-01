"""
回顾功能的REST API接口
"""

from typing import Optional
from datetime import datetime
from database import get_db
from review_service import ReviewService, ReviewExporter


class ReviewAPI:
    """回顾API路由处理器"""
    
    def __init__(self):
        self.routes = []
        self._register_routes()
    
    def _register_routes(self):
        """注册路由"""
        self.routes = [
            ('POST', '/api/reviews/generate', self.generate_review),
            ('GET', '/api/reviews/<review_id>', self.get_review),
            ('GET', '/api/reviews', self.list_reviews),
            ('DELETE', '/api/reviews/<review_id>', self.delete_review),
            ('GET', '/api/reviews/<review_id>/export', self.export_review),
        ]
    
    def generate_review(self, request_data: dict, user_id: int) -> dict:
        """
        生成回顾报告接口
        
        POST /api/reviews/generate
        
        请求参数:
        - review_type: str - 回顾类型 ('monthly' 或 'annual')
        - year: int - 年份
        - month: int (可选) - 月份 (月度回顾时必填)
        - regenerate: bool (可选) - 是否强制重新生成
        
        返回:
        - review_id: int - 回顾报告ID
        - status: str - 生成状态
        - message: str - 提示信息
        """
        try:
            # 获取请求参数
            review_type = request_data.get('review_type')
            year = request_data.get('year')
            month = request_data.get('month')
            regenerate = request_data.get('regenerate', False)
            
            # 参数验证
            if not review_type or not year:
                return {
                    'success': False,
                    'message': '缺少必要参数: review_type 和 year'
                }, 400
            
            if review_type == 'monthly' and not month:
                return {
                    'success': False,
                    'message': '月度回顾必须指定月份'
                }, 400
            
            # 验证时间是否为未来时间
            current_date = datetime.now()
            if review_type == 'monthly':
                if year > current_date.year or (year == current_date.year and month >= current_date.month):
                    return {
                        'success': False,
                        'message': '只能为已结束的时间段生成回顾'
                    }, 400
            else:  # annual
                if year >= current_date.year:
                    return {
                        'success': False,
                        'message': '只能为已结束的年份生成回顾'
                    }, 400
            
            # 获取数据库会话
            db = next(get_db())
            
            try:
                # 创建服务实例
                review_service = ReviewService(db)
                
                # 生成回顾
                review_data = review_service.generate_review(
                    user_id=user_id,
                    review_type=review_type,
                    year=year,
                    month=month,
                    regenerate=regenerate
                )
                
                return {
                    'success': True,
                    'review_id': review_data['review_id'],
                    'status': 'completed',
                    'message': '回顾报告生成成功'
                }, 200
                
            finally:
                db.close()
        
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }, 400
        
        except Exception as e:
            return {
                'success': False,
                'message': f'生成回顾失败: {str(e)}'
            }, 500
    
    def get_review(self, review_id: int, user_id: int) -> dict:
        """
        查询回顾报告接口
        
        GET /api/reviews/<review_id>
        
        返回:
        完整的回顾报告数据
        """
        try:
            # 获取数据库会话
            db = next(get_db())
            
            try:
                # 创建服务实例
                review_service = ReviewService(db)
                
                # 查询回顾
                review_data = review_service.get_review(review_id, user_id)
                
                if not review_data:
                    return {
                        'success': False,
                        'message': '回顾报告不存在或无权访问'
                    }, 404
                
                return {
                    'success': True,
                    'data': review_data
                }, 200
                
            finally:
                db.close()
        
        except Exception as e:
            return {
                'success': False,
                'message': f'查询回顾失败: {str(e)}'
            }, 500
    
    def list_reviews(self, query_params: dict, user_id: int) -> dict:
        """
        回顾列表查询接口
        
        GET /api/reviews
        
        查询参数:
        - review_type: str (可选) - 回顾类型筛选
        - year: int (可选) - 年份筛选
        - page: int (可选) - 页码,默认1
        - page_size: int (可选) - 每页数量,默认10
        
        返回:
        - total: int - 总记录数
        - page: int - 当前页码
        - page_size: int - 每页数量
        - reviews: list - 回顾报告列表
        """
        try:
            # 获取查询参数
            review_type = query_params.get('review_type')
            year = query_params.get('year')
            page = int(query_params.get('page', 1))
            page_size = int(query_params.get('page_size', 10))
            
            # 参数验证
            if page < 1:
                page = 1
            if page_size < 1 or page_size > 100:
                page_size = 10
            
            # 获取数据库会话
            db = next(get_db())
            
            try:
                # 创建服务实例
                review_service = ReviewService(db)
                
                # 查询列表
                result = review_service.list_reviews(
                    user_id=user_id,
                    review_type=review_type,
                    year=int(year) if year else None,
                    page=page,
                    page_size=page_size
                )
                
                return {
                    'success': True,
                    'data': result
                }, 200
                
            finally:
                db.close()
        
        except Exception as e:
            return {
                'success': False,
                'message': f'查询列表失败: {str(e)}'
            }, 500
    
    def delete_review(self, review_id: int, user_id: int) -> dict:
        """
        删除回顾报告接口
        
        DELETE /api/reviews/<review_id>
        
        返回:
        - success: bool - 是否删除成功
        - message: str - 提示信息
        """
        try:
            # 获取数据库会话
            db = next(get_db())
            
            try:
                # 创建服务实例
                review_service = ReviewService(db)
                
                # 删除回顾
                success = review_service.delete_review(review_id, user_id)
                
                if success:
                    return {
                        'success': True,
                        'message': '删除成功'
                    }, 200
                else:
                    return {
                        'success': False,
                        'message': '回顾报告不存在或无权删除'
                    }, 404
                
            finally:
                db.close()
        
        except Exception as e:
            return {
                'success': False,
                'message': f'删除失败: {str(e)}'
            }, 500
    
    def export_review(self, review_id: int, query_params: dict, user_id: int) -> dict:
        """
        导出回顾报告接口
        
        GET /api/reviews/<review_id>/export
        
        查询参数:
        - format: str - 导出格式 ('markdown', 'pdf', 'docx')
        
        返回:
        文件流或错误信息
        """
        try:
            # 获取导出格式
            export_format = query_params.get('format', 'markdown')
            
            if export_format not in ['markdown', 'pdf', 'docx']:
                return {
                    'success': False,
                    'message': '不支持的导出格式'
                }, 400
            
            # 获取数据库会话
            db = next(get_db())
            
            try:
                # 创建服务实例
                review_service = ReviewService(db)
                
                # 查询回顾
                review_data = review_service.get_review(review_id, user_id)
                
                if not review_data:
                    return {
                        'success': False,
                        'message': '回顾报告不存在或无权访问'
                    }, 404
                
                # 导出
                exporter = ReviewExporter()
                
                if export_format == 'markdown':
                    content = exporter.export_to_markdown(review_data)
                    return {
                        'success': True,
                        'format': 'markdown',
                        'content': content,
                        'filename': f"review_{review_id}.md"
                    }, 200
                else:
                    # PDF和DOCX格式暂未实现
                    return {
                        'success': False,
                        'message': f'{export_format}格式导出功能正在开发中'
                    }, 501
                
            finally:
                db.close()
        
        except Exception as e:
            return {
                'success': False,
                'message': f'导出失败: {str(e)}'
            }, 500


# 创建全局API实例
review_api = ReviewAPI()


# 辅助函数:模拟从请求中获取用户ID
def get_current_user_id(request=None) -> int:
    """
    从请求中获取当前用户ID
    实际应用中应该从JWT token或session中获取
    这里提供模拟实现
    """
    # TODO: 实现真实的用户认证逻辑
    return 1  # 暂时返回固定用户ID


# 示例:如何在Flask或FastAPI中使用这些接口
"""
# Flask示例
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/reviews/generate', methods=['POST'])
def api_generate_review():
    user_id = get_current_user_id(request)
    request_data = request.get_json()
    result, status_code = review_api.generate_review(request_data, user_id)
    return jsonify(result), status_code

@app.route('/api/reviews/<int:review_id>', methods=['GET'])
def api_get_review(review_id):
    user_id = get_current_user_id(request)
    result, status_code = review_api.get_review(review_id, user_id)
    return jsonify(result), status_code

@app.route('/api/reviews', methods=['GET'])
def api_list_reviews():
    user_id = get_current_user_id(request)
    query_params = request.args.to_dict()
    result, status_code = review_api.list_reviews(query_params, user_id)
    return jsonify(result), status_code

@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def api_delete_review(review_id):
    user_id = get_current_user_id(request)
    result, status_code = review_api.delete_review(review_id, user_id)
    return jsonify(result), status_code

@app.route('/api/reviews/<int:review_id>/export', methods=['GET'])
def api_export_review(review_id):
    user_id = get_current_user_id(request)
    query_params = request.args.to_dict()
    result, status_code = review_api.export_review(review_id, query_params, user_id)
    return jsonify(result), status_code
"""
